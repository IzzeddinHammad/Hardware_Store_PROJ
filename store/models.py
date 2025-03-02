import uuid
from django.db import models
from django.urls import reverse

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

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