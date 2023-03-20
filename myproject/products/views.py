from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from home.models import profile
from.models import product,cart,Category,Order,Address,OrderItem,variation,Wishlist,coupen,Wallet,Refund
from django.db.models import Count
from django.db.models import Q
from.forms import  CartQuantityForm
import random
from django.http import Http404
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from home.models import User
from django.utils import timezone
import razorpay
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



# Create your views here.


class CategoryView(View):
     def get(self,request,id):
        products=product.objects.filter(category=id)
        title=product.objects.filter(category=id).values('title').annotate(total=Count('title'))
        return render(request,'category.html',locals())

# class product_details(View):
#    def get(self,request,pk):
   
#     category = Category.objects.get(id=pk)
#     products=product.objects.get(pk=pk,category=category)
     
#     allcategory = Category.objects.all()
      
    
            
#     return render(request,"product-details.html",locals())


class product_details(View):
   def get(self, request, pk):
        try:
            products= product.objects.get(pk=pk)
        except product.DoesNotExist:
            raise Http404("Product does not exist")
        
        related_products = product.objects.filter(category=products.category).exclude(pk=pk)[:4]
        allcategory = Category.objects.all()
      
        return render(request, "product-details.html", locals())



   
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
  
    if pid == 0:
        Product = product.objects.all()
        paginator   = Paginator(Product, 4) 
        page        = request.GET.get('page')
        paged_users = paginator.get_page(page)
    else:
     category = Category.objects.get(id=pid)
 

     Product = product.objects.filter(category=category)
   
    allcategory = Category.objects.all()
    context={
        # 'Product':Product,
        'allcategory':allcategory,
        'paged_users' : paged_users,
    
            }
 
    return render(request, "shop.html", context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
             products = product.objects.order_by('id').filter(Q(discription__icontains=keyword) | Q(title__icontains=keyword))
             product_count = products.count()
    context = {
        'Product': products,
        
    }
    return render(request, 'shop.html', context)



def show_cart(request):

    if request.user.is_authenticated:
        
        user = request.user
        items_in_cart = cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 60.0
        total_amount = 0.0
     
        cart_product = [p for p in cart.objects.all() if p.user == user]

        if cart_product:
         for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        coupons = coupen.objects.filter(active=True)
        coupen_id=request.session.get('coupen_id')
        Coupon = None
        if coupen_id:
            Coupon=coupen.objects.get(id=coupen_id)
            discount=int(amount)-int(Coupon.discount)
            print(discount)
            total_amount = discount + shipping_amount
        else:
            discount=0
            total_amount = amount + shipping_amount

        

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
            'coupons':coupons,
            'Coupen' :Coupon,
        }
  
    
        return render(request, 'shop-cart.html', context)
    else:
        return redirect('signin')
   


def remove_cart_item(request,cart_id):
   cart_item = cart.objects.get(id=cart_id)
   cart_item.delete()
   return redirect(show_cart)


def filter_by_size(request):
    selected_size = request.GET.get('size')
    if selected_size:
        products = product.objects.filter(size=selected_size)
    
    else:
        products = product.objects.all()



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

 
   

    # Fetch user's address details
    address = Address.objects.filter(user=request.user)
    wallet_balance = Wallet.objects.get(user=request.user)
    wallet_balanced = wallet_balance.balance
    if wallet_balanced >= grand_total:
        pay=0
    else:
        pay=grand_total-wallet_balanced
    # Handle form submission
    if request.method == 'POST':
        # Handle address form submission
        if request.POST.get('form_type') == 'form2':
            check = request.POST['ad']
            print(check)
            check = check.split('-')
            print(check)
            name = check[0]
            address1 = check[1]
            city = check[2]
            state = check[3]
            post_code = check[4]
            country = check[5]

        else:
            
            new_order = Order()
            Name = request.POST.get('Name')
            Email = request.POST.get('email')
            Add = request.POST.get('address')
            City = request.POST.get('city')
            State = request.POST.get('state')
            Country = request.POST.get('country')
            PostCode= request.POST.get('post_code')
            try :
                value = Address.objects.get(name=Name,address=Add)

            except : 
                value = None
            
          
         
            if value is None:
             
                Address.objects.create(
                user = current_user,
                name = Name,
                address = Add,
                city = City,
                state = State,
                country = Country,
                email = Email,
                postal_code = PostCode
                )
            else :
          

                pass
            new_order.user = current_user
            new_order.name = Name
            new_order.email = Email
            new_order.address = Add
            new_order.city = City
            new_order.state = State
            new_order.country = Country
            new_order.postal_code = PostCode
            new_order.payment_mode = request.POST.get('payment_mode')
            new_order.payment_id = request.POST.get('payment_id')
            new_order.wallet_amt=request.POST.get('wallet_balance')
            new_order.total_price = grand_total

            trackno = 'MINAs' + str(random.randint(1111111, 9999999))
            new_order.tracking_number = trackno
            new_order.save()

            # Create order items and update product stock
            new_order_items = cart.objects.filter(user=current_user)
            for item in new_order_items:
                OrderItem.objects.create(
                    user = current_user,
                    order=new_order,
                    product=item.product,
                    price=item.product.discount_price,
                    quantity=item.quantity
                )
                # Decrease the product from available stock
                order_product = product.objects.filter(id=item.product_id).first()
                order_product.quantity = order_product.quantity - item.quantity
                order_product.save()

            
            
            cart.objects.filter(user=request.user).delete()


            messages.success(request,"Your order has been placed successfully")
            pay_mode=request.POST.get('payment_mode')
            if (pay_mode=="Payment with Razorpay"):
                return JsonResponse({'status':"Your order has been placed successfully"})
            else :
                return JsonResponse({'status':"Your order has been placed successfully"})

      
         

    # Prepare context for rendering template
    instance_value = {
        'cartitems': cartitems,
        'grand_total': grand_total,
        'shipping_amt': shipping_amt,
        'sub_total': sub_total,
        'total': total,
        'quantity': quantity,
        'address': address,
        'name': name,
        'address1': address1,
        'city': city,
        'state': state,
        'post_code': post_code,
        'country': country,
        'wallet_balanced': wallet_balanced,
        'pay':pay 
       
    }
    return render(request, 'checkout.html', instance_value)


def view_product(request):
    Product = product.objects.all()
    cart_items = cart.objects.filter(user=request.user)
    count = len(cart_items)
  
    return render(request, 'view_product.html', locals())



        

def product_filter(request) :
    price1 = (request.GET['min_price'])
    minprice = price1.split('$')
    min_price = minprice[1]
    price2 = (request.GET['max_price'])
    maxprice = price2.split('$')
    max_price = maxprice[1]
    print(min_price)
    print(max_price)
    Product= product.objects.all()
    if min_price and max_price :
        Product =product.objects.filter(discount_price__lte=max_price) 

    context = {
        'Product': Product,
        'min_price': product.objects.all().order_by('discount_price').first().discount_price,
        'max_price': product.objects.all().order_by('-discount_price').first().discount_price,
        'current_min_price': product.objects.all().order_by('discount_price').first().discount_price,
        'current_max_price': product.objects.all().order_by('-discount_price').first().discount_price
    }

    return render(request,'shop.html',context)



def wishlist(request, pk):
    try:
        products = get_object_or_404(product, id=pk)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(products)
        print(products)
    except Exception as e:
        # Handle the error here, e.g. log it or show an error message to the user
        print(f"Error occurred while adding product to wishlist: {e}")
    return redirect('wishlists')


def remove_wishlist(request,pk):
    products = get_object_or_404(product, id=pk)
    wishlist=Wishlist.objects.get(user=request.user)
   
    wishlist.products.remove(products)
    return redirect('wishlists')


def Wishlist_View(request):
    if request.user.is_authenticated:
        try :
            wishlist = Wishlist.objects.get(user=request.user)
            products = wishlist.products.all()
            context = {
                'products': products
            }
            return render(request, 'wishlist.html', context)
        except :
            pass
            return render(request, 'wishlist.html')
            
            
        
    else :
        return redirect('signin')



def coupon(request):
    now = timezone.localtime()
    Coupon = None
    
    if request.method == 'POST':
        Code = request.POST.get('code')
        print(Code)
        try:
            Coupon = coupen.objects.get(code=Code, valid_from__lte=now, valid_to__gte=now)

            request.session['coupen_id'] = Coupon.id
            print(request.session['coupen_id'])
        except coupen.DoesNotExist:
            request.session['coupen_id'] = None
    return redirect('show-cart')


def orders(request):
    if request.user.is_authenticated:
   
        Profile = profile.objects.get(user=request.user)
        orders = Order.objects.filter(user=request.user).order_by('-date_created')
        Cart = cart.objects.filter(user=request.user)
        count = len(Cart)

        context = {
                'orders': orders,
                'Profile': Profile,
                'count': count
            }
        return render(request, 'order.html', context)
    
    else:
      return redirect('signin')

        

def view_orders(request,t_no):
    order=Order.objects.filter(tracking_number=t_no,user=request.user).first()
    orderitems=OrderItem.objects.filter(order=order)
    context={'order':order,'orderitems':orderitems}
    return render(request,'view_orders.html',context)




def view_product_order(request,trackno):
   
    ordernumber=Order.objects.get(user=request.user,tracking_number=trackno)
    print(ordernumber)
    orderitem = OrderItem.objects.filter(order=ordernumber)
    order_count = orderitem.count()
    
    print(orderitem)
    return render(request, 'view_product_order.html' ,locals())


def wallet_balance(request):
    wallet = Wallet.objects.get(user=request.user)
  
   
    balance = wallet.balance
    return render(request, 'wallet.html', locals())







def cancel_order(request, order_id):
    client = razorpay.Client(auth=("rzp_test_k6Ms2BWCn74AHT","aZeXrea3AybLuVTSGEcemHGv"))
    order = get_object_or_404(Order, tracking_number=order_id)
    totals=order.total_price
    wallets=order.wallet_amt
    if wallets == None :
        wallets=0
    else :
        pass
 
 # Calculate the refund amount
    
    refund_amount = float(totals) - float(wallets)
    amounts = refund_amount
    amount=amounts*100
  
 
    pay_mode=order.payment_mode
    print(amount,'this is lasy amount --------------')
    if (pay_mode=="Payment with Razorpay"):


        payment_id=order.payment_id
        captured_payment=client.payment.capture(payment_id,amount)
        refund_data = {
        "payment_id": payment_id,
        "amount": amount,  # amount to be refunded in paise
        "currency": "INR",
      

      # enable speedy refund for instant refunds
            }
        print(refund_data)
        
        refund = client.payment.refund(payment_id,refund_data)

        wallet = Wallet.objects.get(user=request.user)
        
        refunds = totals
        wallet.balance = refunds
        wallet.save()
 
    else:
        refunds=order.total_price
        wallet = Wallet.objects.get(user=request.user)
        refunds = float(refunds)
        wallet.balance += refunds
        wallet.save()
        
     
     # Create a Refund object
    refund = Refund.objects.create(
        order=order,
        amount=refund_amount,
    )
     # Update the order status to "Cancelled"
    order.order_status = 'Cancelled'
    order.save()

    messages.success(request, "Order cancelled successfully. Refund of {} has been processed to your wallet.".format(refund_amount))
    return render(request, 'cancel_order.html', {'refund_amount': refund_amount,'order':order})




  
def razor_pay(request):
    # Get the user's cart and calculate the total amount
    cart_items = cart.objects.filter(user=request.user)
    total = sum(item.product.discount_price * item.quantity for item in cart_items)
    shipping_amt = 60
    sub_total = total
    grand_total = int(sub_total + shipping_amt)

    # Check if the user has enough wallet balance to pay for the order
    wallet_balanced = Wallet.objects.get(user=request.user).balance
 
    if wallet_balanced >= grand_total:
    
        wallet_balance= wallet_balanced - grand_total
        remaining_amount = 0
 
        Wallet.objects.filter(user=request.user).update(balance=wallet_balance)

    else:
      
        # If the user doesn't have enough balance, calculate the remaining amount to be paid
        grand_total -= wallet_balanced
        # Order.objects.filter(user=request.user).update(wallet_amt=0)
        Wallet.objects.filter(user=request.user).update(balance=0)
        remaining_amount = grand_total
        wallet_balance=wallet_balanced
   
    return JsonResponse({
        'success': True,
        'remaining_amount': remaining_amount,
        "wallet_balance" : wallet_balance

        
    })
