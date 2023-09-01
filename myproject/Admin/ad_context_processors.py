# from django.shortcuts import render,redirect
# from products.models import Category,product,Order,OrderItem,Address
# from django.contrib.auth.models import User

# def dashboard(request):
#     # orders=Order.objects.all()
#     users=User.objects.all()
#     products=product.objects.all()
#     # countorder=orders.count()
#     countusers=users.count()
#     cate=Category.objects.all()
#     cate_count=cate.count()


#     countproducts=products.count()

#     context={
#         # "countorder":countorder,
#         "countusers" :countusers,
#         "countproducts" :countproducts,
#         'cate_count': cate_count


        

#     }



#     return context




from django.shortcuts import render, redirect
from products.models import Category, product, Order, OrderItem, Address
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError  # Import the exception

def dashboard(request):
    try:
        # Attempt to retrieve data from the database
        users = User.objects.all()
        products = product.objects.all()
        cate = Category.objects.all()

        countusers = users.count()
        cate_count = cate.count()
        countproducts = products.count()

        context = {
            "countusers": countusers,
            "countproducts": countproducts,
            'cate_count': cate_count,
        }
    except ProgrammingError as e:
        # Handle the exception gracefully (e.g., log the error)
        # You can add custom logic here, like providing default values or rendering an error page.
        context = {
            "error_message": "An error occurred while retrieving data from the database.",
        }

    return context

