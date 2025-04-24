from django.http import JsonResponse
from .models import order

def update_order(tracking_id, status):
    order = Order.objects.get(tracking_id = tracking_id)
    if status in (order.ORDER_STATUS):
        order.status = status
        order.save()
        return JsonResponse("order updated to", status)
    else:
        return JsonResponse('error invalid status')
    
