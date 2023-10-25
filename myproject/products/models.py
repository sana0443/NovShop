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


class variationManager(models.Manager):
    def colors(self):
        return super(variationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(variationManager,self).filter(variation_category='size',is_active=True)


variation_category_choice=(
    ('color','color'),
    ('size','size'),

)

class variation(models.Model):
     product=models.ForeignKey(product,on_delete=models.CASCADE)
     variation_category=models.CharField(max_length=100,choices=variation_category_choice)
     variation_value=models.CharField(max_length=100)
     is_active=models.BooleanField(default=True)
     created_at=models.DateTimeField(auto_now=True)

     objects=variationManager()

     def __str__(self):
        return self. variation_value



class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    variations=models.ManyToManyField(variation) 
    coupon=models.CharField(max_length=100) 

    @property  
    def total_cost(self):
        return self.quantity * self.product.discount_price 



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,null=False)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    phone = models.CharField(validators=[phone_regex], max_length=10, null=True)
    postal_code = models.CharField(max_length=100)


    # def __str__(self) :
    #     return '{}'.format(self.product)
    # def __str__(self):
    #     return '{} {}'.format(self.order.id,self.order.tracking_number)



# class Wishlist(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     products=models.ManyToManyField(product)







