import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from cart.models import Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

stripe.api_key = settings.STRIPE_SECRET_KEY

class orderHistory(LoginRequiredMixin, View):
    def get (self, request):
        if request.user.is_authenticated:
            email =str(request.user.email)
            order_details = Order.objects.filter(emailAddress=email)
        return render(request, 'order_list.html', {'order_details': order_details})


def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    request.session['order_id'] = order.id

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'unit_amount': int(order.total * 100),
                'product_data': {'name': f"Order {order.id}"},
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/order/payment_success/'),
        cancel_url=request.build_absolute_uri('/order/payment_failure/'),
    )

    return redirect(session.url)

def payment_success(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()

        cart_id = request.session.session_key
        if cart_id:
            CartItem.objects.filter(cart__cart_id=cart_id).delete()
            Cart.objects.filter(cart_id=cart_id).delete()
            request.session.flush()

        return render(request, 'order/payment_success.html')

def payment_failure(request):
    return render(request, 'order/payment_failure.html')
