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
    rating = models.FloatField(default=float('0.0'))
    views_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['name', 'author']
