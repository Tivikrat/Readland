import math
import mimetypes
import os
import urllib.parse

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from books.models import Book, UserBook
from pages.forms import AddBookForm
from readland import settings


def get_raiting(book):
    rating = (UserBook.objects.filter(book=book).aggregate(Avg('rating')))['rating__avg']
    if rating is None:
        return 0
    return rating


def get_views_count(book):
    return UserBook.objects.filter(book=book).count()


def main_page(request):
    books = Book.objects.all()
    books_info = []
    for book in books:
        books_info += [{'book': book, 'rating': int(get_raiting(book) * 20), 'views_count': get_views_count(book)}]
    return render(request, 'index.html', {'books_info': books_info})


# Create your views here.
@login_required
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


@login_required
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


@login_required
def read_book(request, book_id):
    return redirect("https://filerender/pdf/index.php?book_url=127.0.0.1:8000/books/" + str(book_id) + "/download")


def view_search(request):
    name = request.GET.get('name', None)
    search = request.GET.get('search', None)
    author = request.GET.get('author', None)
    tag = request.GET.get('tag', None)
    description = request.GET.get('description', None)
    rating = request.GET.get('rating', None)
    rating_gte = request.GET.get('rating_gte', None)
    rating_lte = request.GET.get('rating_lte', None)
    sort_by = request.GET.get('sort_by', 'name')
    sort_type = request.GET.get('sort_type', 'asc')

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

    if ((name or search) or author or tag or description or rating) is not None:
        rating_range = (0.0, 10.0)
        name = search

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

        SORT_CHOICES = [
            'name',
            'author',
            'rating',
            'tag',
            'description'
        ]

        if sort_by in SORT_CHOICES:
            prefix = '-'
            if sort_type == 'asc':
                prefix = ''
            results = Book.objects.filter(**filter_args).order_by(prefix + sort_by)
        else:
            results = Book.objects.filter(**filter_args)

        result_list = list(results)
        book_list = []
        for book in result_list:
            if book.rating == 0.0:
                bookraiting = "Оцінок ще не має"
            else:
                bookraiting = book.rating
            raiting = {
                "number": book.rating,
                "number_raiting": bookraiting,
                "list_raiting": range(int(book.rating)),
                "has_half_star": (book.rating % 1) >= 0.2,
                "empty_stars": range(5 - math.ceil(book.rating))
            }
            book_dict = {"name": book.name,
                         "author": book.author,
                         "date": book.date,
                         "description": book.description,
                         "photo": book.photo,
                         "tag": book.tag,
                         "views_count": book.views_count,
                         "raiting": raiting,
                         "id": book.id
                         }
            book_list.append(book_dict)

        # prequery = [element for element in [name, author, tag, description] if element is not None or '']
        # query = ", ".join(prequery)

        return render(request, 'SearchResult.html', {'results': book_list})
    else:
        return render(request, 'advancedSearch.html')


def view_search_basic(request):
    name = request.GET.get('name', None)
    search = request.GET.get('search', None)
    author = request.GET.get('author', None)
    tag = request.GET.get('tag', None)
    description = request.GET.get('description', None)
    rating = request.GET.get('rating', None)
    rating_gte = request.GET.get('rating_gte', None)
    rating_lte = request.GET.get('rating_lte', None)
    sort_by = request.GET.get('sort_by', 'name')
    sort_type = request.GET.get('sort_type', 'asc')

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

    if ((name or search) or author or tag or description or rating) is not None:
        rating_range = (0.0, 10.0)
        name = search

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

        SORT_CHOICES = [
            'name',
            'author',
            'rating',
            'tag',
            'description'
        ]

        if sort_by in SORT_CHOICES:
            prefix = '-'
            if sort_type == 'asc':
                prefix = ''
            results = Book.objects.filter(**filter_args).order_by(prefix + sort_by)
        else:
            results = Book.objects.filter(**filter_args)

        result_list = list(results)
        book_list = []
        for book in result_list:
            book_dict = dict(book)
            if book.rating == 0.0:
                bookraiting = "Оцінок ще не має"
            else:
                bookraiting = book.rating
            raiting = {
                "number_raiting": bookraiting,
                "list_raiting": range(int(book.rating)),
                "has_half_star": (book.rating % 1) >= 0.2,
                "empty_stars": range(5 - math.ceil(book.rating))
            }
            book_dict["raiting"] = raiting
            book_list.append(book_dict)

        # prequery = [element for element in [name, author, tag, description] if element is not None or '']
        # query = ", ".join(prequery)

        return render(request, 'SearchResult.html', {'results': book_list})
    else:
        return render(request, 'SearchResult.html', {'results': []})


# @login_required
def view_book_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # book.views_count += 1
    # book.save()
    # if request.user.is_authenticated:
    #     user_book = UserBook.objects.filter(user=request.user, book=book)
    #     if user_book.exists():
    #         user_book.update(is_viewed=True)
    #     else:
    #         user_book = UserBook.objects.create(user=request.user, book=book, is_viewed=True)
    #     user_book.save()
    tag = book.tag.split(" ")

    if book.rating == 0.0:
        bookraiting = "Оцінок ще не має"
    else:
        bookraiting = book.rating
    raiting = {
        "number_raiting": bookraiting,
        "list_raiting": range(int(book.rating)),
        "has_half_star": (book.rating % 1) >= 0.2,
        "empty_stars": range(5 - math.ceil(book.rating))
    }
    if request.user.is_authenticated:
        anon = False
    else:
        anon = True
    rating = get_raiting(book)
    if rating is None:
        rating = 0
    views_count = get_views_count(book)
    return render(request, 'bookoverview.html', {"name": book.name,
                                                 "tag": tag,
                                                 "date": book.date,
                                                 "author": book.author,
                                                 "description": book.description,
                                                 "photo": book.photo.url,
                                                 "book": book.file,
                                                 # "rating": rating['rating__avg'],
                                                 "rating": int(rating * 20),
                                                 "views": views_count,
                                                 "anon": anon
                                                 },
                  content_type="text/html")


@login_required
def rate_book(request, book_id, book_rate):
    book = Book.objects.filter(id=book_id).first()
    if request.user.id is not None and 1 <= book_rate <= 5:
        user_book = UserBook.objects.filter(user=request.user, book=book)
        if user_book.exists():
            user_book.update(rating=book_rate)
            user_book.first().save()
        else:
            user_book = UserBook.objects.create(user=request.user, book=book, rating=book_rate)
            user_book.save()
    return redirect('/books/' + str(book_id))
