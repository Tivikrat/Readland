import mimetypes
import os
import urllib.parse

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

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
            return redirect("../books/" + str(book.id))
        else:
            return HttpResponse("Fields was empty: " + str(form.errors))

    return render(request, 'addnewBookScratch.html', {})


def download_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    book_path = os.path.join(settings.MEDIA_ROOT, book.book.name)

    if os.path.exists(book_path):
        with open(book_path, 'rb') as bf:
            mime_type = mimetypes.guess_type(bf.name)

            response = HttpResponse(bf.read(), content_type=mime_type[0])
            response['Content-Disposition'] = \
                "attachment; filename*=UTF-8''" + urllib.parse.quote(os.path.basename(book_path), safe='')

            return response
    raise Http404


def read_book(request, book_id):
    return redirect("https://filerender/pdf/index.php?book_url=127.0.0.1:8000/books/" + str(book_id) + "/download")


def view_book_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.views_count += 1
    book.save()
    tag = book.tag.split(" ")
    return render(request, 'bookoverview.html', {"name": book.name,
                                                 "tag": tag,
                                                 "date": book.date,
                                                 "author": book.author,
                                                 "description": book.description,
                                                 "photo": book.photo.url,
                                                 "book": book.book,
                                                 },
                  content_type="text/html")


def rate_book(request, book_id, book_rate):
    if 1 <= book_rate <= 5:
        Book.objects.filter(pk=book_id).update(rating=book_rate)
    return redirect('/books/' + str(book_id))
