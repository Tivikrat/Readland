from django.urls import path
from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from user_profile import views

urlpatterns = [
                path('<int:user_id>/', views.user_profile),

                # User list

                path('<int:user_id>/list/create/', views.user_list_create),  # Only POST request
                path('<int:user_id>/list/<int:list_id>/update/', views.user_list_update),  # Only POST request
                path('<int:user_id>/list/<int:list_id>/add/<int:book_id>/', views.user_list_add_book),
                path('<int:user_id>/list/<int:list_id>/remove/<int:list_book_id>/', views.user_list_remove_book),
                path('<int:user_id>/list/<int:list_id>/remove/', views.user_list_remove)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
