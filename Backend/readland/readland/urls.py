from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from pages.views import main_page
from readland import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('books/', include('pages.urls')),
                  path('', main_page),
                  # path('accounts/', include('django.contrib.auth.urls')),
                  url(r'^accounts/', include('allauth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
