from django.shortcuts import render


def register(request):
    return render(request,"register.html")

def book_lists(request):
    return render(request,"book_lists.html")

def chbi(request):
    return render(request,"change_book_info.html")