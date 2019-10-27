from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from pages import views

urlpatterns = [
    path('', views.add_book, name='add_book'),
    path('<int:book_id>/download/', views.download_book, name='download_book'),
    path('<int:book_id>/', views.read_book, name='read_book')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)