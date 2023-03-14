from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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
    postal_code = models.CharField(max_length=100)





class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=True)
    address=models.TextField(max_length=300,null=True)
    city=models.CharField(max_length=150,null=True)
    state=models.CharField(max_length=150,null=True)
    country=models.CharField(max_length=150,null=True)
    postal_code=models.CharField(max_length=50,null=True)
    # models.PhoneNumberField(_(""))
    email=models.CharField(max_length=150,null=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
 
    total_price=models.CharField(max_length=50,null=True)
    payment_mode=models.CharField(max_length=50,null=True)
    payment_id=models.CharField(max_length=50,null=True)
    
    order_statuses =(
        ('Pending','Pending'),
        ('Out for shipping','Out for shipping'),
         ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')

    )
    order_status=models.CharField(max_length=50,choices=order_statuses,default='Pending')
    message=models.TextField(null=True)
    tracking_number=models.CharField(max_length=50,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now_add=True)
    wallet_amt=models.FloatField(null=True,default=0)

    def __str__(self):
        return f"{self.tracking_number}"

class OrderItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self) :
        return '{}'.format(self.product)
    # def __str__(self):
    #     return '{} {}'.format(self.order.id,self.order.tracking_number)



# class Wishlist(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     products=models.ManyToManyField(product)

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(product, blank=True)




class coupen(models.Model):
    code=models.CharField(max_length=50)
    discount=models.FloatField()
    valid_from=models.DateTimeField()
    valid_to=models.DateTimeField()
    active=models.BooleanField()


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField()



