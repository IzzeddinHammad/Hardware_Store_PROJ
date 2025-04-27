from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import  post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class order(models.model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "order #{self.id} by {self.user.username}"
    
    def order_notifacations (sender, instance, cerated,  **kwargs ):
        if ordered:
            subject = 'new order'
            message = "Hi {instance.user.username},\n\nthank you for you order of {instance.quantity}x {instance.product_name}"
            our_email ='hardwharestore@gmail.com'
            customer_list = [instance.user.email]

            
            
            send_mail(subject, message, our_email,customer_list)
            
