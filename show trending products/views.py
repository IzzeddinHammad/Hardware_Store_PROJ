from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import product, order


def trending_products(request):
    twenty_days_ago = timezone.now() - timedelta(days=20)


    trending = order.objects.filter(created_on=twenty_days_ago)\
    .values('products')\
    .quantity(quantity=sum('quantity'))\
    .order('-total_quantity')[:5]

    trending_products = product.objects.filter(id=[selection['product']
                                                   for selection in trending])
    
    
    
    product_counts = []
    for product in trending_products:
        total_qty =next(selection['total_qty']
                        for selection in trending
                          if selection['product']==product.id)
        product_counts.append({

            'product': product,
            'total_qty': total_qty
        })

    return render(request, 'trending_products.html',{'product_counts': product_counts})
