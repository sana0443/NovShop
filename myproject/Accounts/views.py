from django.shortcuts import render
from products.models import Category,coupen

# Create your views here.

def home(request):
    
        
        category = Category.objects.all()
        coupons = coupen.objects.filter(active=False)
        print('ggggggggggggggg')
        print(coupons)
        context = {'coupons': coupons,
                'category':category,
                }

    
    
        return render(request,'index.html',context)
