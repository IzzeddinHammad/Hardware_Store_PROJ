from django.urls import path
from .views import process_payment, payment_success, payment_failure
from . import views

urlpatterns = [
    path('pay/<int:order_id>/', process_payment, name='process_payment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failure/', payment_failure, name='payment_failure'),
    path('<int:order_id>/', views.orderDetail.as_view(), name='order_detail'),
    #path('history/', views.orderHistory.as_view(), name='order_history'),
    path('thanks/<int:order_id>',views.thanks , name='thanks'),
]
