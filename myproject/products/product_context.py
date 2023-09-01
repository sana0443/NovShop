from django.shortcuts import render, redirect
from products.models import Category, Product, Order, OrderItem, Address, Wishlist, Cart
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError  # Import the exception

def counts(request):
    wishlist_count = 0
    cart_count = 0
    orderitem_count = 0  # Initialize these variables with default values

    try:
        if request.user.is_authenticated:
            # Try to retrieve data from the database
            wishlists = Wishlist.objects.filter(user=request.user)
            wishlist_count = wishlists.count()

            order = OrderItem.objects.filter(user=request.user)
            orderitem_count = order.count()

            Cart = Cart.objects.filter(user=request.user)
            cart_count = Cart.count()
    except ProgrammingError as e:
        # Handle the exception gracefully (e.g., log the error)
        # You can add custom logic here, like providing default values or rendering an error page.
        pass

    contxt = {
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
        'orderitem_count': orderitem_count,
    }

    return contxt
