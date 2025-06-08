from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Book
from .forms import BookForm


class BookListView(generic.ListView):
    model = Book
    template_name = "books/book_list_page.html"    
    context_object_name = 'books'
    paginate_by = 4

    def get_queryset(self):
        return Book.objects.all().order_by('-modified_datetime')


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = "books/book_detail_page.html"


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_create_page.html"
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_update_page.html"

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = "books/book_delete_page.html"

    def get_success_url(self):
        return reverse("books:book_list")  
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookSearchView(generic.ListView):
    model = Book
    template_name = "books/book_search.html"
    context_object_name = 'books'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(category__icontains=query)
            ).order_by('-modified_datetime')
        return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context