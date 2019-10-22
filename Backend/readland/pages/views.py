from django.http import HttpResponse
from django.shortcuts import render

from books.models import Book
from pages.forms import AddBookForm


# Create your views here.
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return HttpResponse('Book has been saved')
        else:
            return HttpResponse("Form is not valid")

    return render(request, 'addnewBookScratch.html', {})
