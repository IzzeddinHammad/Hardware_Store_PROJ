from store import models as store_models
from customer import models as customer_models

def default(request):
    category_ = store_models.Category.objects.all()
    try:
        cart_id = request.session['cart_id']
        total_cart_items = store_models.Cart.objects.filter(cart_id=cart_id).count()
    except:
        total_cart_items = 0

    try:
        wishlist_count = customer_models.Wishlist.objects.filter(user=request.user)
    except:
        wishlist_count = 0

    return {
        "total_cart_items": total_cart_items,
        "category_": category_,
        "wishlist_count": wishlist_count,
    }