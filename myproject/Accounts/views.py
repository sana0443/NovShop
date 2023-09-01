from django.shortcuts import render
from products.models import Category,coupen



def home(request):
    
        
        # category = Category.objects.all()
        # coupons = coupen.objects.filter(active=True)
       
        # context = {'coupons': coupons,
        #         'category':category,
        #         }
        pass
    
    
        return render(request,'index.html')
