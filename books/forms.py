from django.forms import ModelForm

from .models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "user",
            "title",
            "author",
            "translator",
            "publisher",
            "price",
            "body",
        ]