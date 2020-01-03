from django.shortcuts import render


def book_lists(request):
    return render(request, "book_lists.html", {"uid": request.user.id})


def chbi(request):
    return render(request, "change_book_info.html", {"uid": request.user.id})
