from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Book, Review
from .forms import BookForm, ReviewForm
from django.shortcuts import get_object_or_404, render, redirect

class BookListView(generic.ListView):
    model = Book
    template_name = "books/book_list_page.html"    
    context_object_name = 'books'
    paginate_by = 4

    def get_queryset(self):
        return Book.objects.all().order_by('-modified_datetime')

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/book_detail_page.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['review_form'] = ReviewForm()
        return context
    

class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        review = form.save(commit=False)
        review.book = book
        review.user = self.request.user
        review.save()
        Book.update_rating(book)
        return redirect(book.get_absolute_url())
    
    def form_invalid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return redirect(book.get_absolute_url())
  
        
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