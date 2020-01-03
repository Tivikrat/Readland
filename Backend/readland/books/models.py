from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core import validators
from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, null=True)
    date = models.DateField()
    author = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='book_previews', null=True)
    file = models.FileField(upload_to='books')
    rating = models.FloatField(default=0, null=False)
    views_count = models.IntegerField(default=0)
    price = models.IntegerField(default=100)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'author']


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField(blank=True, null=True,
                             validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    is_bought = models.BooleanField(default=False)
    is_viewed = models.BooleanField(blank=True, default=False)
