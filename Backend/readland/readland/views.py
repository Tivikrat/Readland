from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from user_profile.models import UserList


@login_required
def book_lists(request):
    lists = UserList.objects.filter(user=request.user)
    print(lists)
    return render(request, "book_lists.html", {"lists": lists, "user": request.user})


@login_required
def chbi(request):
    return render(request, "change_book_info.html", {"uid": request.user.id})
