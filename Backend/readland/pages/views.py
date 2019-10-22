from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def add_book(request):
    if request.method == 'POST':
        return HttpResponse("123")

    return render(request, 'addnewBookScratch.html', {})
