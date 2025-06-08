from django.contrib import admin
from .models import Book, Review

from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'average_rating', 'created_datetime']
    list_filter = ['category', 'language', 'status']
    search_fields = ['title', 'author', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']