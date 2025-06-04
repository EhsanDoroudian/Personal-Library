from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model



class Book(models.Model):
    UserModel = get_user_model()

    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='book')
    title = models.CharField(verbose_name='title', max_length=50)
    body = models.TextField(verbose_name='description')
    author = models.CharField(verbose_name='author', max_length=30)
    category = models.CharField(verbose_name='category', max_length=50, null=True)
    page_num = models.PositiveIntegerField(verbose_name='page number', null=True)
    shabak_num = models.CharField(verbose_name="shabak number", max_length=20, unique=True, null=True)
    publisher = models.CharField(verbose_name='publisher', max_length=20, null=True)
    translator = models.CharField(verbose_name='translator', max_length=30, null=True)
    year = models.DateField(verbose_name='year of publish', null=True, blank=True)
    cover = models.ImageField(upload_to='covers', blank=True, null=True)
    price = models.DecimalField(verbose_name='price', max_digits=6, decimal_places=2)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("books:book_detail", args=[self.id])