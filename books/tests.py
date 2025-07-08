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
        self.assertEqual(new_book.title, 'New Book')
        self.assertEqual(new_book.body, 'New Body')
        self.assertEqual(new_book.author, 'New Author')
        self.assertEqual(new_book.category, 'New Category')
        self.assertEqual(new_book.publisher, 'New Publisher')
        self.assertEqual(new_book.translator, 'New Translator')
        self.assertEqual(new_book.status, 'readed')

        self.assertEqual(response.url, new_book.get_absolute_url())  # Check redirect URL

    def test_book_create_form_invalid(self):
        self.client.force_login(self.user1)
        # Submit empty data to trigger validation errors
        response = self.client.post(reverse('books:book_create'), data={})
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertTemplateUsed(response, 'books/book_create_page.html')
        self.assertEqual(Book.objects.all().count(), 2)  # No book created
        self.assertTrue(response.context['form'].errors)  # Form has errors

    def test_book_create_post_unauthenticated(self):
        book_data = {
            'title': 'New Book',
            'body': 'New Body',
            'author': 'New Author',
            'category': 'New Category',
            'publisher': 'New Publisher',
            'translator': 'New Translator',
            'status': 'readed'  # Adjust if status is not a valid field
        }
        response = self.client.post(reverse('books:book_create'), data=book_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/books/create/')
        self.assertEqual(Book.objects.all().count(), 2)  # No book created


class BookUpdateTest(BookTest):
    def test_book_update_url_unauthenticated(self):
        response = self.client.get(reverse('books:book_update', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/books/update/{self.book1.id}/')

    def test_book_update_authenticated_owner(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_update', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)

    def test_book_update_template_used(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_update', kwargs={'pk': self.book1.id}))
        self.assertTemplateUsed(response, 'books/book_update_page.html')

    def test_book_update_context(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_update', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], BookForm)
        self.assertEqual(response.context['object'], self.book1)

    def test_book_update_form_submission(self):
        self.client.force_login(self.user1)
        update_data = {
            'title': 'Updated Book',
            'body': 'Updated body',
            'author': 'Updated Author',
            'category': 'Non-Fiction',
            'publisher': 'Updated Publisher',
            'translator': 'Updated Translator',
            'status': 'readed'  # Adjust if status is not a valid field
        }
        response = self.client.post(reverse('books:book_update', kwargs={'pk': self.book1.id}), data=update_data)

        if response.status_code != 302:
            self.fail(f"Form submission failed: {response.context['form'].errors}")
            
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.book1.refresh_from_db()  # Refresh to get updated values
        self.assertEqual(self.book1.title, 'Updated Book')
        self.assertEqual(self.book1.body, 'Updated body')
        self.assertEqual(self.book1.author, 'Updated Author')
        self.assertEqual(self.book1.category, 'Non-Fiction')
        self.assertEqual(self.book1.publisher, 'Updated Publisher')
        self.assertEqual(self.book1.translator, 'Updated Translator')
        self.assertEqual(self.book1.status, 'readed')  # Adjust if status is not a field
        self.assertEqual(self.book1.user, self.user1)  # User should remain unchanged
        # Check redirect (assumes get_absolute_url points to book_detail)
        self.assertRedirects(response, reverse('books:book_detail', kwargs={'pk': self.book1.id}))

    def test_book_update_form_invalid(self):
        self.client.force_login(self.user1)
        # Submit empty data to trigger validation errors
        response = self.client.post(reverse('books:book_update', kwargs={'pk': self.book1.id}), data={})
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertTemplateUsed(response, 'books/book_update_page.html')
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Book One')  # Original title unchanged
        self.assertTrue(response.context['form'].errors)  # Form has errors

    def test_book_update_non_owner(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('books:book_update', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 403)  # Forbidden for non-owner

    def test_book_update_post_non_owner(self):
        self.client.force_login(self.user2)
        update_data = {
            'title': 'Unauthorized Update',
            'body': 'Unauthorized body',
            'author': 'Unauthorized Author',
            'category': 'Unauthorized Category',
            'publisher': 'Unauthorized Publisher',
            'translator': 'Unauthorized Translator',
            'status': 'readed'
        }
        response = self.client.post(reverse('books:book_update', kwargs={'pk': self.book1.id}), data=update_data)
        self.assertEqual(response.status_code, 403)  # Forbidden for non-owner
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Book One')  # Original title unchanged

    def test_book_update_invalid_pk(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_update', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class BookDeleteTest(BookTest):
    def test_book_delete_url_unauthenticated(self):
        response = self.client.get(reverse('books:book_delete', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/books/delete/{self.book1.id}/')
    
    def test_book_delete_authenticated_owner(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_delete', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_book_delete_template_used(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_delete', kwargs={'pk': self.book1.id}))
        self.assertTemplateUsed(response, 'books/book_delete_page.html')

    def test_book_delete_form_submission(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('books:book_delete', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())  # Book deleted
        self.assertRedirects(response, reverse('books:book_list'))  # Redirect to book list

    def test_book_delete_non_owner(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('books:book_delete', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 403)  # Forbidden for non-owner

    def test_book_delete_post_non_owner(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('books:book_delete', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, 403)  # Forbidden for non-owner
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())  # Book not deleted

    def test_book_delete_invalid_pk(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('books:book_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Non-existent book

    def test_book_delete_post_invalid_pk(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('books:book_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)  # Non-existent book


class ReviewTest(BookTest):
    def test_review_view_form(self):
        self.client.force_login(self.user1)
        url = reverse('books:review_create', kwargs={'pk': self.book2.id})  
        response = self.client.post(  
            path=url,
            data={
            "user": self.user1,
            "book": self.book2,
            "comment": 'Great book!',
            "rating": 5,
            "created_at": timezone.now()
            },
        )
        
        # Debug: Print form errors if status is not 302
        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors)
        
        self.assertEqual(response.status_code, 302)  # Should redirect
        new_review = Review.objects.last()
        self.assertIsNotNone(new_review) 
        self.assertEqual(new_review.user.id, self.user1.id)
        self.assertEqual(new_review.book.id, self.book2.id)
        self.assertEqual(new_review.comment, 'Great book!')
        self.assertEqual(new_review.rating, 5)
        self.assertEqual(response.url, self.book2.get_absolute_url())  # Check redirect URL
        self.assertRedirects(response, self.book2.get_absolute_url()) 


    def test_review_create_form_invalid(self):
        self.client.force_login(self.user1)
        # Submit empty data to trigger validation errors
        url = reverse('books:review_create', kwargs={'pk': self.book2.id})  
        response = self.client.post(path=url, data={})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.book2.get_absolute_url())
        self.assertRedirects(response, self.book2.get_absolute_url()) 
        self.assertEqual(Review.objects.all().count(), 2) 
