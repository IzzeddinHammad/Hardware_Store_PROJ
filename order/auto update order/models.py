from django.db import models
from .track    import unique_tracking_id

class order(models.Model):
    ORDER_STATUS = [
        ('processing'),
        ('shipped'),
        ('delevered'),

]
    tracking_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20, CHOICES= ORDER_STATUS, defult='processing')
    date_made = models.DateTimeField(auto_now_add=True)


    def store_info(self, ):
        if not self.tracking_id:
            self.tracking_id = unique_tracking_id(order)
            super().save()

            

