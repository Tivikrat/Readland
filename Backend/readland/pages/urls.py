from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('', views.add_book, name='add_book'),
    path('<int:book_id>/download', views.download_book, name='download_book'),
]
