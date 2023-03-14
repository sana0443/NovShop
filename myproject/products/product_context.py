from django.shortcuts import render,redirect
from products.models import Category,product,Order,OrderItem,Address,Wishlist,cart
from django.contrib.auth.models import User


def counts(request):
    
    wishlists=Wishlist.objects.all()
    wishlist_count=wishlists.count()

    order=OrderItem.objects.all()
    orderitem_count=order.count()


    Cart=cart.objects.all()
    cart_count=Cart.count()

    contxt={
        'wishlist_count':wishlist_count,
        'cart_count':cart_count,
        'orderitem_count':orderitem_count
    }

    return contxt

