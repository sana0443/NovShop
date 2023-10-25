from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from products.models import Category,product
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import auth
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
    return render(request, 'Adminside/add_products.html' , dic)

def adminHome(request):
    return render(request, 'Adminside/Adbase.html')   
 

def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        if Category.objects.filter(name__iexact=name.lower().replace(' ','')).exists():
          msg = "Category already exists"
        else:
         Category.objects.create(name=name)
         msg = "Category added"
    return render(request, 'Adminside/add_category.html', locals())



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

def logoutadmin(request):
        auth.logout(request)
        return render(request,'home.html')


def error(request,exception):
    return render(request,'error.html')

   