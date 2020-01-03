import json
import math
import mimetypes
import os
import string
import urllib.parse
import random
from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from liqpay.liqpay3 import LiqPay

from books.models import Book, UserBook
from pages.forms import AddBookForm, UpdateBookForm
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
    if request.user.is_authenticated:
        anon = False
    else:
        anon = True

    for book in books:
        books_info += [{'book': book, 'rating': int(get_raiting(book) * 20), 'views_count': get_views_count(book)}]
    return render(request, 'index.html', {'books_info': books_info,
                                          "anon": anon, 'user_id': request.user.id})


# Create your views here.
@login_required
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            return redirect("../books/" + str(book.id))
        else:
            return HttpResponse("Fields were empty: " + str(form.errors))

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


def extract_message(json_object, name):
    value = json_object.get(name, "")
    if value != "":
        value = value[0]['message']
    return value


def format_errors(form_errors_str):
    form_errors = json.loads(form_errors_str)
    errors = namedtuple('errors', ['name', 'tag', 'date', 'description', 'photo', 'file', 'price'])
    name = extract_message(form_errors, 'name')
    tag = extract_message(form_errors, 'tag')
    date = extract_message(form_errors, 'date')
    description = extract_message(form_errors, 'description')
    photo = extract_message(form_errors, 'photo')
    file = extract_message(form_errors, 'file')
    price = extract_message(form_errors, 'price')
    return errors(name=name, tag=tag, date=date, description=description, photo=photo, file=file, price=price)


@login_required
def add_book(request):
    if request.method == "GET":
        return render(request, "change_book_info.html",
                      {"breadcrumb": "Добавление издания"})
    if request.method == "POST":
        add_book_form = AddBookForm(data=request.POST, files=request.FILES)
        if add_book_form.is_valid():
            book = add_book_form.save(commit=False)
            book.created_by = request.user
            book.save()
            return redirect(f"/books/{book.id}")
        else:
            return render(request, "change_book_info.html",
                          {"breadcrumb": "Добавление издания",
                           "errors": format_errors(add_book_form.errors.as_json())})


@login_required
def read_book(request, book_id):
    return redirect("https://filerender/pdf/index.php?book_url=127.0.0.1:8000/books/" + str(book_id) + "/download")


@login_required
def update_book(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)

    allow_edit = False
    if user is not None and user.is_authenticated and hasattr(user, 'id') and user.id is not None and \
            book.created_by == user or user.is_superuser:
        allow_edit = True

    if request.method == "GET":
        return render(request, "change_book_info.html",
                      {"breadcrumb": "Изменение издания", "book": book})
    elif request.method == 'POST' and allow_edit:
        update_book_form = UpdateBookForm(data=request.POST, files=request.FILES, instance=book)

        if update_book_form.is_valid():
            book = update_book_form.save(commit=False)
            book.save()
            return redirect(f"/books/{book.id}")
        return render(request, "change_book_info.html",
                      {"breadcrumb": "Изменение издания", "book": book,
                       "errors": format_errors(update_book_form.errors.as_json())})


@login_required
def delete_book(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)

    allow_edit = False
    if user is not None and user.is_authenticated and hasattr(user, 'id') and user.id is not None and \
            book.created_by == user or user.is_superuser:
        allow_edit = True

    if allow_edit:
        book.delete()

        return redirect("/")
    else:
        raise PermissionDenied()


def book_suggestions(request):
    book_name = request.GET.get('name', None)

    if book_name is not None:
        books = Book.objects.filter(name__icontains=book_name).values()
    else:
        books = Book.objects.all().values()

    return JsonResponse(list(books), safe=False)


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


def view_manage(request, book_id):
    return render(request, 'change_book_info.html')


# @login_required
def view_book_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_rating = 0
    # book.views_count += 1
    # book.save()
    user_book = None
    bought = False
    if request.user.is_authenticated:
        try:
            user_book = UserBook.objects.get(user=request.user, book=book)

            if not user_book.is_viewed:
                user_book.is_viewed = True
                user_book.save()

            if user_book.is_bought:
                bought = True
            user_rating = user_book.rating
        except UserBook.DoesNotExist:
            user_book = UserBook.objects.create(user=request.user, book=book, is_viewed=True)
            user_book.save()

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
    signature = None
    data = None
    price = None
    if request.user.is_authenticated:
        anon = False

        if user_book is not None and not user_book.is_bought:
            liqpay = LiqPay(settings.LIQPAY_SANDBOX_PUBLIC_KEY, settings.LIQPAY_SANDBOX_PRIVATE_KEY)
            price = book.price
            params = {
                "version": 3,
                "action": "pay",
                "amount": str(price),
                "currency": "UAH",
                "description": book.name,
                "order_id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + "___" + str(
                    request.user.id) + "___" + str(book.id),
                "type": "buy",
                'server_url': str(request.build_absolute_uri("/") + 'billing/pay-callback/'),
                'result_url': str(request.build_absolute_uri("/") + 'billing/pay-callback/'),
                "language": "uk"
            }
            data = liqpay.cnb_data(params)
            signature = liqpay.cnb_signature(params)
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
                                                 "rating": int(rating * 20) if rating != float('NaN') else 0,
                                                 "views": views_count,
                                                 "anon": anon,
                                                 "bought": bought,
                                                 "payment_form": {
                                                     'signature': signature,
                                                     'data': data,
                                                     'price': price
                                                 },
                                                 'user_rating': user_rating,
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
