from django import forms
from books.models import Book


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'tag', 'date', 'author', 'description', 'photo', 'file', 'price']


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'tag', 'author', 'description', 'photo', 'file', 'price']
