from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'author', 'price', 'create_datetime']
    ordering = ['modified_datetime']