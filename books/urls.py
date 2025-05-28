from django.urls import path, include

from . import views


app_name = 'books'

urlpatterns = [
    path('', view=views.BookListView.as_view(), name="book_list")
]