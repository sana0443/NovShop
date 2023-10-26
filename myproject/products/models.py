from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']


class product(models.Model):
    quantity = models.PositiveIntegerField(null=True)
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    discription=models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, default='medium')
    product_image=models.ImageField(upload_to='product')

    def __str__(self):
        return self.title



class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    coupon=models.CharField(max_length=100) 

    @property  
    def total_cost(self):
        return self.quantity * self.product.discount_price 










