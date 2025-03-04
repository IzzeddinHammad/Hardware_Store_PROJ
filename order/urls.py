from django.urls import path
from .views import process_payment, payment_success, payment_failure

urlpatterns = [
    path('pay/<int:order_id>/', process_payment, name='process_payment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failure/', payment_failure, name='payment_failure'),
]
