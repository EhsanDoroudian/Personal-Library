from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'created_datetime']
    list_display_links = ['id', 'title']