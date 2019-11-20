import math
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

    book_path = os.path.join(settings.MEDIA_ROOT, book.file.name)

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


def view_search(request):
    name = request.GET.get('name', None)
    author = request.GET.get('author', None)
    tag = request.GET.get('tag', None)
    description = request.GET.get('description', None)
    rating = request.GET.get('rating', None)
    rating_gte = request.GET.get('rating_gte', None)
    rating_lte = request.GET.get('rating_lte', None)

    if rating is not None:
        try:
            rating = float(rating)
        except ValueError:
            rating = None

    if rating_gte is not None:
        try:
            rating_gte = float(rating_gte)
        except ValueError:
            rating_gte = None

    if rating_lte is not None:
        try:
            rating_lte = float(rating_lte)
        except ValueError:
            rating_lte = None

    if (name or author or tag or description or rating) is not None:
        rating_range = (0.0, 10.0)

        if rating_gte is not None:
            rating_range = (rating_gte, 10.0)
        elif rating_lte is not None:
            rating_range = (0.0, rating_lte)

        if rating:
            filter_args = {
                'name__icontains': name if name is not None else '',
                'author__contains': author if author is not None else '',
                'tag__contains': tag if tag is not None else '',
                'description__contains': description if description is not None else '',
                'rating__range': rating_range,
                'rating': rating
            }
        else:
            filter_args = {
                'name__icontains': name if name is not None else '',
                'author__contains': author if author is not None else '',
                'tag__contains': tag if tag is not None else '',
                'description__contains': description if description is not None else '',
                'rating__range': rating_range
            }

        results = Book.objects.filter(**filter_args)

        return render(request, 'results.html', {'results': results})
    else:
        return render(request, 'advancedSearch.html')

def view_search_basic(request):
    return render(request, 'SearchResult.html')


def view_book_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if(book.rating == 0.0):
        bookraiting = "Оцінок ще не має"
    else:
        bookraiting = book.rating
    raiting = {
        "number_raiting": bookraiting,
        "list_raiting": range(int(book.rating)),
        "has_half_star": (book.rating % 1) >= 0.2,
        "empty_stars": range(5-math.ceil(book.rating))
    }
    book.views_count += 1
    book.save()
    tag = book.tag.split(" ")

    return render(request, 'bookoverview.html', {"name": book.name,
                                                 "tag": tag,
                                                 "date": book.date,
                                                 "author": book.author,
                                                 "description": book.description,
                                                 "photo": book.photo.url,
                                                 "book": book.file,
                                                 "raiting": raiting,
                                                 "views": book.views_count,
                                                 },
                  content_type="text/html")


def rate_book(request, book_id, book_rate):
    if 1 <= book_rate <= 5:
        Book.objects.filter(pk=book_id).update(rating=book_rate)
    return redirect('/books/' + str(book_id))
