from django.urls import path
from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from billing.views import PayCallbackView

urlpatterns = [
                  path('pay-callback/', PayCallbackView.as_view(), name="pay_callback_view")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
