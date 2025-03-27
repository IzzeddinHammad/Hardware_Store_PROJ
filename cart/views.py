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
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults={'quantity': 0})

    if product.stock < cart_item.quantity + 1:
        return render(request, 'insufficient_stock.html', {'product': product})

    cart_item.quantity += 1
    cart_item.save()
    product.stock -= 1
    product.save()

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
    cart_items = CartItem.objects.filter(cart=cart, active=True) if cart else []
    total = sum(item.product.price * item.quantity for item in cart_items)
    counter = sum(item.quantity for item in cart_items)

    discount = 0
    voucher_id = 0
    new_total = 0
    voucher=None

    voucher_apply_form = VoucherApplyForm()


    try:
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id)
        if voucher != None:
            discount = (total*(voucher.discount/Decimal('100')))
            new_total = (total - discount)
            stripe_total = int(new_total * 100)
    except:
        ObjectDoesNotExist
        pass

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter, 'voucher_apply_form': voucher_apply_form, 'new_total': new_total, 'voucher': voucher, 'discount':discount})



def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    cart_item = CartItem.objects.filter(product=product, cart=cart).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            product.stock += 1
            cart_item.save()
        else:
            product.stock += cart_item.quantity
            cart_item.delete()
        product.save()

    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    cart_item =  CartItem.objects.filter(product=product, cart=cart).first()
    if cart_item:
        product.stock += cart_item.quantity
        product.save()
        cart_item.delete()
    return redirect('cart:cart_detail')

def empty_cart(request):
    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            item.product.stock += item.quantity
            item.product.save()
        cart.delete()
    return redirect('/products/')

def checkout(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    if not cart_items.exists():
        return redirect('cart:cart_detail')

    total = sum(item.quantity * item.product.price for item in cart_items)
    order = Order.objects.create(total=total, emailAddress=request.user.email)
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
