from django.forms import ModelForm

from .models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "body",
            "author",
            "category",
            "page_num",
            "shabak_num",
            "publisher",
            "translator",
            "year",
            "cover",
            "price",
        ]