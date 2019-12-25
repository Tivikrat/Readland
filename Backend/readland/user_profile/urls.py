from django.urls import path
from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from user_profile import views

urlpatterns = [
                  path('<int:user_id>/', views.user_profile),
                  path('<int:user_id>/edit', views.edit),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
