import stripe
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
import uuid
from django.urls import reverse
from order.models import Order, OrderItem 
from stripe import StripeError
from django.core.exceptions import ObjectDoesNotExist



stripe.api_key = settings.STRIPE_SECRET_KEY

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
    
    return redirect('cart:cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except Cart.DoesNotExist:
        pass
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter})

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart:cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=uuid.UUID(str(product_id)))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    
    cart_item.delete()
    
    return redirect('cart:cart_detail')

def empty_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        #cart.cartitem_set.all().delete()
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        cart_items.delete()
        cart.delete()
        return redirect('store:product_list')
    except Cart.DoesNotExist:
        pass

    return redirect('cart:cart_detail')

def checkout(request):
    if request.method == 'POST':
        total = 100
        stripe_total = int(total * 100)
        description = 'Hardware Store - Order Payment'

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order from Hardware Store',
                        },
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                billing_address_collection='required',
                success_url=request.build_absolute_uri(reverse('store:product_list')),
                cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, 'cart/cart.html', {'error': str(e)})

    return render(request, 'cart/cart.html')

def create_order(request):
    try:
        session_id = request.GET.get('session_id')
        if not session_id:
            raise ValueError("Session ID not found")
        
        try:
            session = stripe.checkout.Session.retrieve(session_id) 
        except StripeError as e:
            return redirect("store:product_list")
        
        customer_details = session.customer_details 
        if not customer_details or not customer_details.address: 
            raise ValueError("Missing information in the Stripe session.")
        
        billing_address = customer_details.address 
        billing_name = customer_details.name 
        shipping_address = customer_details.address
        shipping_name = customer_details.name 

        try: 
            order_details = Order.objects.create(
                token=session.id, 
                total = session.amount_total / 100, 
                emailAddress= customer_details.email, 
                billingName = billing_name, 
                billingAddress1 = billing_address.line1, 
                billingCity = billing_address.city, 
                billingPostcode = billing_address.postal_code, 
                billingCountry = billing_address.country, 
                shippingName = shipping_name, 
                shippingAddress1=shipping_address.line1, 
                shippingCity=shipping_address.city, 
                shippingPostcode=shipping_address.postal_code,
                shippingCountry=shipping_address.country,

            ) 
            order_details.save()
        except Exception as e:
            print(f"Error: {e}" )
            return redirect("store:product_list")
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, active=True)
        except ObjectDoesNotExist:
            return redirect("store:product_list")
        except Exception as e:
            print(f"Error: {e}")
            return redirect("store:product_list")
        
        for item in cart_items:
            try:
                oi = OrderItem.objects.create(
                    product=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                    order=order_details
                )
                oi.save()
                product = Product.objects.get(id=item.product.id)
                product.stock = int(item.product.stock - item.quantity)
                product.save()
                empty_cart(request)
            except Exception as e:
                return redirect("store:product_list")
        return redirect('store:all_products')
    
    except ValueError as ve:
        print(f"Error: {ve}")
        return redirect("store:product_list")
    except StripeError as se:
        print(f"Stripe Error: {se}")
        return redirect("store:product_list") 

    except Exception as e:
        print(f"Unexpected error: {e}")
        return redirect("store:product_list") 

            
