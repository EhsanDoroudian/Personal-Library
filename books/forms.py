from django import forms
from .models import Book, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'body', 'author', 'category', 'page_num', 'shabak_num', 'publisher', 'translator', 'year', 'price', 'language', 'status', 'cover']
        widgets = {
            'year': forms.NumberInput(attrs={'placeholder': 'مثال: 1390', 'min': 1300, 'max': 1404}),
        }
    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']