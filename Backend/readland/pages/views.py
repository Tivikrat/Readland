import mimetypes
import os

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from books.models import Book
from pages.forms import AddBookForm
from readland import settings


# Create your views here.
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return HttpResponse('Book has been saved. Book ID = ' + str(book.id))
        else:
            print(form.errors)
            return HttpResponse("Form is not valid")

    return render(request, 'addnewBookScratch.html', {})


def download_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    book_path = os.path.join(settings.MEDIA_ROOT, book.book.name)

    if os.path.exists(book_path):
        with open(book_path, 'rb') as bf:
            mime_type = mimetypes.guess_type(bf.name)

            response = HttpResponse(bf.read(), content_type=mime_type[0])
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(book_path)

            return response
    raise Http404
