from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import CustomUserModel


UserModel = get_user_model()

class Book(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='book')
    title = models.CharField(verbose_name='title', max_length=50)
    author = models.CharField(verbose_name='author', max_length=50)
    translator = models.CharField(verbose_name='translator', max_length=50)
    publisher = models.CharField(verbose_name='publisher', max_length=30)
    price = models.DecimalField(verbose_name='price', max_digits=6, decimal_places=2)
    body = models.TextField(verbose_name='body', default=None)
    create_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("books:book_detail", args=[self.id])