from django.shortcuts import render,redirect

from django.views import View
from.models import product,cart,Category
from django.contrib import messages
from home.models import User
from django.contrib.auth.models import auth
from django.core.paginator import Paginator
from django.http import JsonResponse



# Create your views here.


class CategoryView(View):
     def get(self,request,id):
        products=product.objects.filter(category=id)
        return render(request,'category.html',locals())

   
def add_to_cart(request, prod_id):
    Product = product.objects.get(id=prod_id)

    if request.user.is_authenticated:
        user = request.user
        is_cart_exists = cart.objects.filter(product=Product, user=user).exists()
    else:
        return redirect('signin')

    if is_cart_exists:
        cart_item = cart.objects.get(user=user, product=Product)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = cart.objects.create(product=Product, quantity=1, user=user)
    
    return redirect('show-cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            item_quantity = request.POST.get('item_quantity')

            try:
                cart_item = cart.objects.get(id=item_id, user=user)
                cart_item.quantity = item_quantity
                cart_item.save()

                # Calculate the new total amount for the cart item
                new_total_amount = cart_item.quantity * cart_item.product.discount_price

                # Recalculate the cart total
                items_in_cart = cart.objects.filter(user=user)
                amount = sum(cart.quantity * cart.product.discount_price for cart in items_in_cart)

                return JsonResponse({'total_amount': new_total_amount, 'cart_amount': amount})
            except cart.DoesNotExist:
                return JsonResponse({'error': 'Cart item not found'}, status=400)

        else:
            items_in_cart = cart.objects.filter(user=user)
            amount = sum(cart.quantity * cart.product.discount_price for cart in items_in_cart)
            total_amount = amount

            context = {
                'items_in_cart': items_in_cart,
                'total_amount': total_amount,
                'amount': amount,
            }

            return render(request, 'shop-cart.html', context)
    else:
        return redirect('signin')


def remove_cart_item(request,cart_id):
   cart_item = cart.objects.get(id=cart_id)
   cart_item.delete()
   return redirect(show_cart)




def products(request,pid):
  
    allcategory = Category.objects.all()

    if pid == 0:
        Product = product.objects.all()
       
    else:
        allcategory = Category.objects.all()
        category = Category.objects.get(id=pid)
        Product = product.objects.filter(category=category)

    paginator = Paginator(Product, 4) 
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)

    return render(request, "shop.html", locals())








