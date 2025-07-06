from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime

from accounts.models import CustomUserModel
from books.forms import ReviewForm, BookForm
from books.models import Book, Review


class BookTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user1 = CustomUserModel.objects.create_user(
            username='username1', 
            email='email1@gmail.com',
            password='password123'
        )
        cls.user2 = CustomUserModel.objects.create_user(
            username='username2', 
            email='email2@gmail.com',
            password='password123'
        )
        cls.admin = CustomUserModel.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin1234'
        )

        # Create sample books for testing
        cls.book1 = Book.objects.create(
            user=cls.user1,
            title='Book One',
            body='Body one',
            author='Author One',
            category='Category1',
            publisher='Publisher1',
            translator='Translator1',
            modified_datetime=timezone.now() - datetime.timedelta(days=1)
        )
        cls.book2 = Book.objects.create(
            user=cls.user1,
            title='Book Two',
            body='Body two',
            author='Author Two',
            category='Category2',
            publisher='Publisher2',
            translator='Translator2',
            modified_datetime=timezone.now()
        )

        # Create sample reviews for book1
        cls.review1 = Review.objects.create(
            user=cls.user1,
            book=cls.book1,
            comment='Great book!',
            rating=5,
            created_at=timezone.now()
        )
        cls.review2 = Review.objects.create(
            user=cls.user2,
            book=cls.book1,
            comment='Good read.',
            rating=3,
            created_at=timezone.now()
        )

class BookListTest(BookTest):
    def test_book_list_urls(self):
        response = self.client.get('')
        response2 = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_book_list_name(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)

    def test_book_list_template_used(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertTemplateUsed(response, 'books/book_list_page.html')

    def test_book_list_contains(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book One')
        self.assertContains(response, 'Author One')
        self.assertIn(self.book1, response.context['books'])
        self.assertIn(self.book2, response.context['books'])

    def test_book_list_empty(self):
        # Delete all books to test empty list
        Book.objects.all().delete()
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 0)

    def test_book_list_pagination(self):
        # Create more books to test pagination (paginate_by = 4)
        for i in range(3, 7):  # Create 4 more books (total 6)
            Book.objects.create(
                user=self.user1,
                title=f'Book {i}',
                body=f'Body {i}',
                author=f'Author {i}',
                category='Category',
                publisher='Publisher',
                translator='Translator',
                modified_datetime=timezone.now()
            )
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 4)  # First page has 4 books
        self.assertTrue(response.context['is_paginated'])
        # Test second page
        response = self.client.get(reverse('books:book_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 2)  # Second page has 2 books

    def test_book_list_ordering(self):
        response = self.client.get(reverse('books:book_list'))
        books = response.context['books']
        # Verify books are ordered by modified_datetime descending
        self.assertEqual(books[0], self.book2)  # Newer book first
        self.assertEqual(books[1], self.book1)  # Older book second


class BookDetailTest(BookTest):
    def test_book_detail_url_name(self):
        response = self.client.get(reverse('books:book_detail', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_template_used(self):
        response = self.client.get(reverse('books:book_detail', kwargs={'pk': self.book1.id}))
        self.assertTemplateUsed(response, 'books/book_detail_page.html')

    def test_book_detail_content(self):
        response = self.client.get(reverse('books:book_detail', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book1.title)
        self.assertContains(response, self.book1.author)
        self.assertContains(response, self.book1.body)
        self.assertContains(response, self.review1.comment)
        self.assertContains(response, self.review2.comment)

    def test_book_detail_context(self):
        response = self.client.get(reverse('books:book_detail', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book'], self.book1)
        self.assertEqual(len(response.context['reviews']), 2)  # Two reviews for book1
        self.assertIsInstance(response.context['review_form'], ReviewForm)
        self.assertEqual(response.context['num_reviews'], 2)
        self.assertEqual(response.context['avg_rating'], 4.0)  # (5 + 3) / 2

    def test_book_detail_no_reviews(self):
        response = self.client.get(reverse('books:book_detail', kwargs={'pk': self.book2.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['reviews']), 0)
        self.assertEqual(response.context['num_reviews'], 0)
        self.assertEqual(response.context['avg_rating'], 0)  # As per view logic

    def test_book_detail_invalid_pk(self):
        # Test with a non-existent book ID
        response = self.client.get(reverse('books:book_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class BookCreateTest(BookTest):
    def test_book_create_view_url_unauthenticated_users(self):
        response = self.client.get('/create/')
        response2 = self.client.get('/books/create/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/create/')
        self.assertRedirects(response2, '/accounts/login/?next=/books/create/')

    def test_book_create_view_name_unauthenticated_users(self):
        response = self.client.get(reverse('books:book_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/books/create/')

    def test_book_view_authenticated_users(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_create'))
        self.assertEqual(response.status_code, 200)

    def test_book_view_authenticated_template_used(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("books:book_create"))
        self.assertTemplateUsed(response, 'books/book_create_page.html')

    def test_book_create_context(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("books:book_create"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], BookForm)
    
    def test_book_view_form(self):
        self.client.force_login(self.user1)
        url = reverse('books:book_create')  
        response = self.client.post(  
            path=url,
            data={
                'user': self.user1,
                'title ': 'New Book',
                'body': 'New Body',
                'author': 'New Author',
                'category': 'New Category',
                'publisher': 'New Publisher',
                'translator': 'New Translator',
                'status': 'readed'
            },
        )
        
        # Debug: Print form errors if status is not 302
        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors)
        
        self.assertEqual(response.status_code, 302)  # Should redirect
        new_book = Book.objects.last()
        self.assertIsNotNone(new_book)  # Ensure Book was created
        self.assertEqual(Book.objects.last().user, self.user1)
        self.assertEqual(Book.objects.last().title, 'New Book')
        self.assertEqual(Book.objects.last().body, 'New Body')
        self.assertEqual(Book.objects.last().author, 'New Author')
        self.assertEqual(Book.objects.last().category, 'New Category')
        self.assertEqual(Book.objects.last().publisher, 'New Publisher')

        self.assertEqual(response.url, new_book.get_absolute_url())  # Check redirect URL
