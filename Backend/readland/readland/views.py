from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from user_profile.models import UserList
from user_profile.views import get_list_image_preview


@login_required
def book_lists(request):
    lists = UserList.objects.filter(user=request.user)
    for books_list in lists:
        books = []
        for list_book in books_list.list_books.all():
            if len(books) > 2:
                break
            else:
                books += [list_book.book]
        list_name = f"uploaded/lists/{books_list.id}"
        if len(books) > 0:
            get_list_image_preview(*[book.photo.path for book in books], string_list_name=list_name)
        else:
            get_list_image_preview("uploaded/lists/-1.png", string_list_name=list_name)
    return render(request, "book_lists.html", {"lists": lists, "user": request.user})


@login_required
def chbi(request):
    return render(request, "change_book_info.html", {"uid": request.user.id})
