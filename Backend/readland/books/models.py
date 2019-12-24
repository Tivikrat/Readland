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
    rating = models.FloatField(null=True)
    views_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['name', 'author']


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField(blank=True, default=float('NaN'),
                             validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    is_viewed = models.BooleanField(blank=True, default=False)
