# Generated by Django 5.2.1 on 2025-06-10 13:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0006_alter_book_shabak_num"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="book",
            unique_together={("title", "author")},
        ),
    ]
