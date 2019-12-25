from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from liqpay.liqpay3 import LiqPay

from books.models import UserBook
from readland import settings


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_SANDBOX_PUBLIC_KEY, settings.LIQPAY_SANDBOX_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_SANDBOX_PRIVATE_KEY + data + settings.LIQPAY_SANDBOX_PRIVATE_KEY)
        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            book_id = response.get("order_id", None).split("___")[2]
            user_id = response.get("order_id", None).split("___")[1]
            if response.get("err_code", None) == "err_card_receiver_def" or\
                    response.get("status", None) == "success":
                try:
                    user_book = UserBook.objects.get(user_id=user_id, book_id=book_id)
                    if not user_book.is_bought:
                        user_book.is_bought = True
                        user_book.save()
                except UserBook.DoesNotExist:
                    user_book = UserBook.objects.create(user_id=user_id, book_id=book_id, is_bought=True)
                    user_book.save()

                return redirect("/books/" + book_id + "/")
            else:
                return redirect("/books/" + book_id + "/")

        return HttpResponse()
