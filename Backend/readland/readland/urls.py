from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from pages.views import main_page
from readland import settings

import pages.views as pw

from readland.views import  register,book_lists,chbi

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('books/', include('pages.urls')),
                  path('user/', include('user_profile.urls')),
                  path('', main_page),

                  # новые страницы, двиньте их когда будет время
                  path('register', register),
                  path('book_lists', book_lists),
                  path('chbi', chbi),
                  # path('accounts/', include('django.contrib.auth.urls')),
                  url(r'^accounts/', include('allauth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
