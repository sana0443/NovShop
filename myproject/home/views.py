from django.shortcuts import render,redirect
# from Accounts.views import home
from products.views import cart,products
from.models import profile
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
# from.models import signup
from .forms import SignUpForm
from. models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account is created for {user.username}')
            return render(request, 'index.html')
        else:
            messages.warning(request, 'Registration failed. Please correct the errors below.')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})



def Signin(request):
        
        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']

            user=authenticate(username=username,password=password)
            
            if user is not None:
                 login(request,user)
                 messages.success(request,f'Welcome , {user.username}')
                
                 return render(request, 'index.html')  

            else:
                 messages.info(request,'username or password is incorrect')
                 return render(request, 'login.html') 
        else:
                return render(request,'login.html')        




def logoutuser(request):
        auth.logout(request)
        return redirect(Signin)


