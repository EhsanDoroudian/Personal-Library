from django.urls import path

from . import views


app_name = 'books'

urlpatterns = [
    path('', view=views.BookListView.as_view(), name="book_list"),
    path('books/<int:pk>/',view=views.BookDetailView.as_view(), name='book_detail'),   
    path('search/', view=views.BookSearchView.as_view(), name='book_search'),
    path('create/', view=views.BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>/', view=views.BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/', view=views.BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/review/',view=views.ReviewCreateView.as_view(), name='review_create'),
]