from django.shortcuts import render,redirect
from products.models import Category,product,Order,OrderItem,Address
from django.contrib.auth.models import User

def dashboard(request):
    orders=Order.objects.all()
    users=User.objects.all()
    products=product.objects.all()
    countorder=orders.count()
    countusers=users.count()

    countproducts=products.count()

    context={
        "countorder":countorder,
        "countusers" :countusers,
        "countproducts" :countproducts,


        

    }



    return context





