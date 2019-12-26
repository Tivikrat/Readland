from django.contrib.auth import get_user_model
from django.db import models
from books.models import Book


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='User', null=False)
    last_name = models.CharField(max_length=255, default='Anonymous', null=False)
    mobile_phone = models.CharField(max_length=13, null=True)
    about_user = models.TextField(null=True)
    balance = models.FloatField(null=False, default=0)
    photo = models.ImageField(upload_to='users', null=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' (ID: ' + str(self.user.id) + ', ' + self.user.username + ')'


class UserList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Список користувача', null=False)

    def __str__(self):
        return self.name


class UserListBook(models.Model):
    list = models.ForeignKey(UserList, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.list.name + ' (' + str(self.list.user.id) + ') - ' + self.book.name
