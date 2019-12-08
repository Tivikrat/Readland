from django.urls import path
from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from pages import views

urlpatterns = [
                  path('', views.add_book),
                  path('<int:book_id>/read/', views.read_book),
                  path('<int:book_id>/download/', views.download_book),
                  path('<int:book_id>/', views.view_book_info),
                  path('<int:book_id>/rate/<int:book_rate>', views.rate_book),
                  path('search/', views.view_search, name="search"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
