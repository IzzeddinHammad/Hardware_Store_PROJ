from django.db import models
from django.contrib.auth.models import User

class product(models.model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    
    
    def __str__ (self):
        return self.name
    


class order(models.model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
