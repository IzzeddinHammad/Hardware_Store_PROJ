from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/products/",null=True, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    stock = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])



class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveBigIntegerField(default=3)
    comment = models.TextField()
    # creation_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.comment