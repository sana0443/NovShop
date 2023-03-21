from django.shortcuts import render,redirect
from products.models import Category,product,Order,OrderItem,Address,Wishlist,cart
from django.contrib.auth.models import User


def counts(request):
    
    if request.user.is_authenticated :
        wishlists=Wishlist.objects.filter(user=request.user)
        wishlist_count=wishlists.count()

        order=OrderItem.objects.filter(user=request.user)
        orderitem_count=order.count()

    

        Cart=cart.objects.filter(user=request.user)
        cart_count=Cart.count()
    else :

        wishlist_count=0
        cart_count=0
        orderitem_count=0

    contxt={
        'wishlist_count':wishlist_count,
        'cart_count':cart_count,
        'orderitem_count':orderitem_count,
       
    }

    return contxt

