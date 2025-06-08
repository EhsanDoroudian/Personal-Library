from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'translator', 'publisher', 'category', 'page_num', 'year', 'language', 'body', 'cover', 'price', 'status']
        widgets = {
            'year': forms.NumberInput(attrs={'placeholder': 'مثال: 1390', 'min': 1300, 'max': 1404}),
        }