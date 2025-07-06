from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.db.models import Count, Avg


class Book(models.Model):
    UserModel = get_user_model()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='کاربر'
    )
    title = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True, verbose_name='اسلاگ', blank=True, null=True)
    body = models.TextField(verbose_name='توضیحات')
    author = models.CharField(max_length=50, verbose_name='نویسنده')
    category = models.CharField(max_length=50, verbose_name='دسته بندی', blank=True)
    page_num = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد صفحه')
    shabak_num = models.CharField(
        max_length=16,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{10,13}$', 'شابک باید ۱۰ یا ۱۳ رقمی باشد.')],
        verbose_name='شابک'
    )
    publisher = models.CharField(max_length=50, blank=True, verbose_name='ناشر')
    translator = models.CharField(max_length=50, blank=True, verbose_name='مترجم')
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name='سال انتشار')  # Changed to PositiveIntegerField
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='جلد')
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت')
    language = models.CharField(max_length=50, default='فارسی', verbose_name='زبان', blank=True)
    status = models.CharField(
        max_length=30,
        choices=[('readed', 'خوانده شده'), ('borrowed', 'قرض داده شده'), ('not readed', 'خوانده نشده')],
        default='readed',
        verbose_name='وضعیت',
    )
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب‌ها'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['shabak_num']),
        ]
        unique_together = [['title', 'author']]
        
    def __str__(self):
        return f"{self.title} - {self.author}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("books:book_detail", args=[self.id])

class Review(models.Model):
    REVIEW_STATUS_WATING = 'w'
    REVIEW_STATUS_APPROVED = 'a'
    REVIEW_STATUS_NOT_APPROVED = 'na' 
    REVIEW_STATUS = [
        (REVIEW_STATUS_WATING, 'wating'),
        (REVIEW_STATUS_APPROVED, 'approved'),
        (REVIEW_STATUS_NOT_APPROVED, 'not approved')
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='کتاب'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='کاربر'
    )
    rating = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name='امتیاز'
    )
    comment = models.TextField(verbose_name='نظر')
    status = models.CharField(max_length=3, choices=REVIEW_STATUS, default=REVIEW_STATUS_APPROVED, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        unique_together = [['book', 'user']]  # Prevent multiple reviews by same user
        indexes = [
            models.Index(fields=['book', 'user']),
        ]

    def __str__(self):
        return f"نظر {self.user.username} برای {self.book.title}"