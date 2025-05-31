from django.urls import path, include

from . import views


app_name = 'books'

urlpatterns = [
    path('', view=views.BookListView.as_view(), name="book_list"),
    path('<int:pk>/', view=views.BookDetailView.as_view(), name='book_detail'),
    path('create/', view=views.BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>', view=views.BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>', view=views.BookDeleteView.as_view(), name='book_delete'),
]