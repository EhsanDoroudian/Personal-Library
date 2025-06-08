from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'translator', 'publisher', 'category', 'page_num', 'year', 'shabak_num', 'language', 'body', 'cover', 'price', 'status']
        widgets = {
            'year': forms.NumberInput(attrs={'placeholder': 'مثال: 2023', 'min': 1000, 'max': 9999}),
        }