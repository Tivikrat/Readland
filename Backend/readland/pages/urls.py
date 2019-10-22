from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('', views.add_book, name='add_book'),
]
