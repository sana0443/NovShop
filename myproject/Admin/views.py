from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from products.models import Category,product,Order,OrderItem,Address
from home.models import profile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import timedelta, date
from django.db.models import Count
from django.db.models import Q



from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('admin_dashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'Adminside/admin_dsbd.html' , dic)

def adminHome(request):
    return render(request, 'Adminside/Adbase.html')   

def admin_dashboard(request):
    return render(request, 'Adminside/admin_dsbd.html') 


def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        if Category.objects.filter(name__iexact=name.lower().replace(' ','')).exists():
          msg = "Category already exists"
        else:
         Category.objects.create(name=name)
         msg = "Category added"
    return render(request, 'Adminside/add_category.html', locals())

def view_category(request):

    if request.method == 'POST':
      keyword = request.POST['keyword']
      category= Category.objects.filter(Q(name__icontains=keyword) |  Q(created__icontains=keyword) ).order_by('name')

    
    else:
        category = Category.objects.all().order_by('name')
  
    paginator   = Paginator(category, 2) 
    page        = request.GET.get('page')
    paged_users = paginator.get_page(page)
  
    
    return render(request, 'Adminside/view_category.html',locals())


def edit_product(request, pid):
    Product = product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            Product.product_image = image
            Product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        product.objects.filter(id=pid).update(title=name, selling_price=price, discount_price=discount, category=catobj, discription=desc)
        messages.success(request, "Product Updated")
    return render(request, 'Adminside/edit_product.html', locals())




def edit_category(request, pid):
  if Category.objects.filter(name__iexact=name.lower().replace(' ', '')).exists():
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
    return render(request, 'Adminside/edit_category.html', locals())
 
def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('view_category') 


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ['name', 'description']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        search_query = request.GET.get('q')
        if search_query:
            qs = qs.filter(name__icontains=search_query)
        return qs


def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        product.objects.create(title=name,selling_price=price, discount_price=discount, discription=desc,category=catobj,product_image=image)
        messages.success(request, "Product added")
    return render(request, 'Adminside/add_products.html', locals())



def view_product(request):

    if request.method == 'POST':
      keyword = request.POST['keyword']
      order = product.objects.order_by('id').filter(Q(title__icontains=keyword) |  Q(category__name__icontains=keyword)  |  Q(discount_price__icontains=keyword) )
    else:

     order = product.objects.all().order_by('-id')
    paginator   = Paginator(order, 5) 
    page        = request.GET.get('page')
    paged_users = paginator.get_page(page)
    return render(request, 'Adminside/view_product.html', locals())

def delete_product(request, pid):
    Product = product.objects.get(id=pid)
    Product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')


def manage_order(request):

    if request.method == 'POST':
      keyword = request.POST['keyword']
      orders = Order.objects.order_by('id').filter(Q(name__icontains=keyword) |  Q(order_status__icontains=keyword)  |  Q(id__icontains=keyword) )
    else:
     orders=Order.objects.all().order_by('id')

    action = request.GET.get('action', 0)
    order = Order.objects.filter(order_status=int(action))
    order_statuses = Order.order_statuses
    Order_status = order_statuses[int(action)-1][1]
    paginator   = Paginator(orders, 5) 
    page        = request.GET.get('page')
    paged_users = paginator.get_page(page)

    

    if int(action) == 0:
        orders = Order.objects.filter()
        order_status = 'All'
      
    return render(request, 'Adminside/order_manage.html', locals()) 

def admin_view_order(request,trackno):
    orders=Order.objects.get(tracking_number=trackno)
    address=Order.objects.filter(user=request.user).first
   
    orderitem=OrderItem.objects.filter(order=orders)
    context={
    'orderitem':orderitem,
    'orders':orders,
    'address':address
    }
    return render(request,'Adminside/admin_view_order.html',context)


def order_shipping(request,trackno):
    
    order = Order.objects.get(tracking_number=trackno)
    order.order_status = 'Out for shipping'
    order.save()
    return redirect('order_manage')

def order_delivered(request, trackno):
    order = Order.objects.get(tracking_number=trackno)
    order.order_status = 'Delivered'
    order.save()
    return redirect('order_manage')


def order_cancelled(request, trackno):
    order = Order.objects.get(tracking_number=trackno)
    order.order_status = 'Delivered'
    order.save()
    return redirect('order_manage')

def order_shipped(request, trackno):
    order = Order.objects.get(tracking_number=trackno)
    order.order_status = 'Shipped'
    order.save()
    return redirect('order_manage')



def manage_user(request):
    
    if request.method == 'POST':
      keyword = request.POST['keyword']
      users = profile.objects.filter(Q(name__icontains=keyword) |  Q(email__icontains=keyword) | Q(phone__icontains=keyword)).order_by('id')

    
    else:
        users = profile.objects.order_by('id')

    paginator   = Paginator(users, 1) 
    page        = request.GET.get('page')
    paged_users = paginator.get_page(page)

    context = {
        'users' : paged_users,
    }
    return render(request, 'Adminside/user_management.html', context)




def block_user(request, user_id):
      user = profile.objects.get(id=user_id)
      if user.user.username != 'admin':

       
        user.is_active = False
        user.save()

      return redirect('manage_user')

   


def unblock_user(request, user_id):

        user = profile.objects.get(id=user_id)
        user.is_active = True
        user.save()

        return redirect('manage_user')

   