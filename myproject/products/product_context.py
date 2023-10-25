from django.shortcuts import render, redirect
from products.models import Category, product,  Address, cart
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError  # Import the exception

def counts(request):
    cart_count = 0
    try:
        if request.user.is_authenticated:
           

            Cart = cart.objects.filter(user=request.user)
            cart_count = Cart.count()
    except ProgrammingError as e:
       
        pass

    contxt = {
    
        'cart_count': cart_count,
      
    }

    return contxt
