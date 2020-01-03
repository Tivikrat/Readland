from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from pages.views import main_page
from readland import settings

import pages.views as pw

from readland.views import book_lists, chbi
from user_profile.views import change_profile, profile

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('books/', include('pages.urls')),
                  path('billing/', include('billing.urls')),
                  path('user/', include('user_profile.urls')),
                  path('', main_page),

                  # новые страницы, двиньте их когда будет время
                  path('change_profile', change_profile),
                  path('profile', profile),
                  path('book_lists', book_lists),
                  path('chbi', chbi),
                  # path('accounts/', include('django.contrib.auth.urls')),
                  url(r'^accounts/', include('allauth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
