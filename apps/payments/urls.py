from django.urls import path
from .views import payment_page, payment_success, payment_failed, process_payment

urlpatterns = [
    path("", payment_page, name="payment_page"),
    path("success/", payment_success, name="payment_success"),
    path("failed/", payment_failed, name="payment_failed"),
    path("process/", process_payment, name="process_payment"),
]