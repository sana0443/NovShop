from django.shortcuts import render,redirect

from django.views import View
from.models import product,cart,Category,variation
from django.contrib import messages
from home.models import User
from django.contrib.auth.models import auth
from django.core.paginator import Paginator



# Create your views here.


class CategoryView(View):
     def get(self,request,id):
        products=product.objects.filter(category=id)
        return render(request,'category.html',locals())

   
def add_to_cart(request, prod_id):
  Product = product.objects.get(id=prod_id)

  if request.method=='POST':
    product_variation=[]
    for item in request.POST:
        key=item
        value=request.POST[key]
        print(key,value)
       
        try:
            Variation=variation.objects.get(product=Product,variation_category__iexact=key,variation_value__iexact=value)
          
            product_variation.append(Variation)
        except:
            pass

   
    if request.user.is_authenticated:
       
        user = request.user
        is_Cart_exists=cart.objects.filter(product=Product,user=user).exists()
    else:
        return redirect('signin')
    if is_Cart_exists:
        Cart = cart.objects.filter(user=user, product=Product)
        ex_var_list=[]
        id=[]
        for item in Cart:
            existing_variation=item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            print(ex_var_list)
        if product_variation in ex_var_list:
            index=ex_var_list.index(product_variation)
            item_id=id[index]
            item=cart.objects.get(product=Product,id=item_id)
            item.quantity+=1
            item.save()
            return redirect('show-cart')
           
        else:
            item=cart.objects.create(product=Product,quantity=1,user=user)
            if len(product_variation)>0:
             item.variations.clear()
             item.variations.add(*product_variation)
             item.save()
            return redirect('show-cart')

        
    else:
         Cart = cart.objects.create(user=user, product=Product, quantity=1)
         Cart.save()
       
         if len(product_variation)>0:
            Cart.variations.clear()
            Cart.variations.add(*product_variation)
            Cart.save()
         return redirect('show-cart')

  else: # GET request
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





def show_cart(request):

    if request.user.is_authenticated:
        user = request.user
        items_in_cart = cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 60.0
        total_amount = 0.0
        coupenamt= 0
        cart_product = [p for p in cart.objects.all() if p.user == user]

        if cart_product:
         for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
       
   
       
            discount=0
            total_amount = amount + shipping_amount
            coupenamt=0

        

        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            item_quantity = request.POST.get('item_quantity')

            cart_item = cart.objects.get(id=item_id)
            cart_item.quantity = item_quantity
            cart_item.save()

            return redirect('show-cart')

        context = {
            'items_in_cart': items_in_cart,
            'total_amount': total_amount,
            'amount': amount,
            'coupen' :coupenamt,
         
        }
  
    
        return render(request, 'shop-cart.html', context)
    else:
        return redirect('signin')
   


def remove_cart_item(request,cart_id):
   cart_item = cart.objects.get(id=cart_id)
   cart_item.delete()
   return redirect(show_cart)


def place_order(request):
    current_user=(request.user)
    cartitems=cart.objects.filter(user=request.user)
    grand_total=0
    shipping_amt=60
    sub_total=0
    total=0
    total_price=0
    name=""
    address1=""
    city = ""
    state = ""
    post_code= ""
    country=""
    quantity=0
    
    for item in cartitems:
        total += (item.product.discount_price * item.quantity)
        quantity += item.quantity
    sub_total = total
    grand_total = int(sub_total + shipping_amt)

 
   



def view_product(request):
    Product = product.objects.all()
    cart_items = cart.objects.filter(user=request.user)
    count = len(cart_items)
  
    return render(request, 'view_product.html', locals())



