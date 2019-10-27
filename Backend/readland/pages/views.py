import mimetypes
import os


from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from books.models import Book
from pages.forms import AddBookForm
from readland import settings
from PIL import Image


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


def get_image(request, image_path):
    try:
        with open('uploaded/book_previews/' + image_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGB', (1, 1), (255, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response


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


def read_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # book_path = os.path.join(settings.MEDIA_ROOT, str(book.photo))
    #
    # with open(book.photo.path, 'rb') as bf:
    #     mime_type = mimetypes.guess_type(bf.name)

    br = ""
    for i in range(book.rating):
        br += str(i)
    # book_path = os.path.join(settings.MEDIA_ROOT, book.book.name)
    # book.photo = book_path
    # fields = {
    #     "name",
    #     "tag",
    #     "date",
    #     "author",
    #     "description",
    #     "photo",
    #     "book",
    #     "rating",
    # }
    tag = book.tag.split(",")
    return render(request, 'bookoverview.html', {"name": book.name,
                                                 "tag": tag,
                                                 "date": book.date,
                                                 "author": book.author,
                                                 "description": book.description,
                                                 "photo": book.photo.url,
                                                 "book": book.book,
                                                 "rating_list": br,
                                                 "rating": book.rating
                                                 },
                  content_type="text/html")
