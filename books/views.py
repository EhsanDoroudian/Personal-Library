from django.views import generic
from django.urls import reverse
from .models import Book
from .forms import BookForm


class BookListView(generic.ListView):
    model = Book
    template_name = "books/book_list_page.html"    
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.all().order_by('-modified_datetime')


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/book_detail_page.html"


class BookCreateView(generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_create_page.html"


class BookUpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_update_page.html"


class BookUpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_update_page.html"


class BookDeleteView(generic.DeleteView):
    model = Book
    template_name = "books/book_delete_page.html"

    def get_success_url(self):
        return reverse("books:book_list")