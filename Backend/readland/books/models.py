from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='book_previews')
    book = models.FileField(upload_to='books')

    class Meta:
        unique_together = ['name', 'author']
