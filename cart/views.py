import stripe
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
import uuid
from django.urls import reverse
from order.models import Order, OrderItem
from stripe.error import StripeError
from django.core.exceptions import ObjectDoesNotExist

stripe.api_key = settings.STRIPE_SECRET_KEY

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults={'quantity': 1})

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
    cart_items = CartItem.objects.filter(cart=cart, active=True) if cart else []
    total = sum(item.product.price * item.quantity for item in cart_items)
    counter = sum(item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter})

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    cart_item = CartItem.objects.filter(product=product, cart=cart).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    CartItem.objects.filter(product=product, cart=cart).delete()
    return redirect('cart:cart_detail')

def empty_cart(request):
    Cart.objects.filter(cart_id=_cart_id(request)).delete()
    return redirect('/products/')

def checkout(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    if not cart_items.exists():
        return redirect('cart:cart_detail')

    total = sum(item.quantity * item.product.price for item in cart_items)
    order = Order.objects.create(total=total, emailAddress="test@example.com")
    request.session['order_id'] = order.id

    return redirect('process_payment', order_id=order.id)

def create_order(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('/products/')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        customer_details = session.customer_details
        if not customer_details or not customer_details.address:
            return redirect('/products/')

        order_details = Order.objects.create(
            token=session.id,
            total=session.amount_total / 100,
            emailAddress=customer_details.email,
            billingName=customer_details.name,
            billingAddress1=customer_details.address.line1,
            billingCity=customer_details.address.city,
            billingPostcode=customer_details.address.postal_code,
            billingCountry=customer_details.address.country,
            shippingName=customer_details.name,
            shippingAddress1=customer_details.address.line1,
            shippingCity=customer_details.address.city,
            shippingPostcode=customer_details.address.postal_code,
            shippingCountry=customer_details.address.country,
        )
        order_details.save()

        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart, active=True)
            for item in cart_items:
                OrderItem.objects.create(
                    product=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                    order=order_details
                )
                product = Product.objects.get(id=item.product.id)
                product.stock = max(0, product.stock - item.quantity)
                product.save()

            cart.delete()

        return redirect('order:thanks' , order_details.id)

    except (ObjectDoesNotExist, StripeError, Exception) as e:
        return redirect('/products/')
