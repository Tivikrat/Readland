from django.contrib import admin
from books.models import Book, UserBook

# Register your models here.
admin.site.register(Book)
admin.site.register(UserBook)
