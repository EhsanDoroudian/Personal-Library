from django.contrib import admin
from django.db.models import Count
from .models import Book, Review
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib import admin


admin.site.site_header = "Library"
admin.site.index_title = "Special Access"


class ReviewInline(admin.TabularInline):
    model = Review
    fields = ['user', 'rating', 'comment']
    extra = 2

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'price_status', 'num_of_reviews']
    list_per_page = 10
    list_filter = ['category', 'language', 'status']
    list_editable = ['price']
    ordering = ['created_datetime']
    search_fields = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ReviewInline]

    def get_queryset(self, request):
        return super().get_queryset(request)\
        .prefetch_related('reviews')\
        .annotate(
            reviews_count = Count('reviews')
        )

    def price_status(self, book: Book):
        if book.price < 100000:
            return 'low'
        if book.price > 500000:
            return 'high'
        return 'medium'
    
    @admin.display(description='تعداد نظرات', ordering='reviews_count')
    def num_of_reviews(self, book:Book):
        url = (
            reverse('admin:books_review_changelist')
            + '?'
            +urlencode({
                'book__id': book.id,
            })
        )

        return format_html('<a href="{}">{}</a>', url, book.reviews_count)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_book', 'user', 'rating', 'status', 'created_at']
    list_filter = ['rating', 'created_at']
    list_editable = ['status']
    list_select_related = ['book']

    @admin.display(description='عنوان کتاب')
    def review_book(self, review):
        return review.book.title