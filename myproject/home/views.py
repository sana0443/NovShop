from django.shortcuts import render,redirect
from Accounts.views import home
from products.views import cart
from.models import profile
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
# from.models import signup
import random
from django.http import JsonResponse
from django.core.mail import EmailMessage
from .forms import SignUpForm,UserUpdate,profileUpdate
from. models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from.forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm





def Signin(request):
        
        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']

          
            user=authenticate(username=username,password=password)
            
            if user is not None:
                 login(request,user)
                
                 return redirect(home)

            else:
                 messages.info(request,'username or password is incorrect')
                 return redirect('signin')
        else:
                return render(request,'login.html')        

def logoutuser(request):
        auth.logout(request)
        return redirect(home)


def signup(request):
    usr = None
    
    if request.method=='POST':
                get_otp=request.POST.get('otp')
                

                if get_otp:
                  
                  get_usr=request.POST.get('usr')
                  
                  usr=User.objects.get(username=get_usr)
                  

                  if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                    usr.is_active=True
                    usr.save()
                    messages.success(request,f'Account is created for{usr.username}')
                    return redirect(Signin)
                  else:
                    messages.warning(request,f'You Entered a wrong OTP')
                    return render(request,'signup.html',{'otp':True,'usr':usr})
                                          
                
                
                form = SignUpForm(request.POST)
               
                if form.is_valid():
                 
                 form.save()
                 username=form.cleaned_data.get('username')
                 
                 name=form.cleaned_data.get('name')
                 usr=User.objects.get(username=username)
                 usr.email=username
                 usr.username=username
                 if len(name)>1:
                   usr.last_name=name[1]
                 usr.is_active=False
                 usr.save()
                 usr_otp=random.randint(100000,999999)
                 UserOTP.objects.create(user=usr,otp=usr_otp)

                 mess=f'Hello\t{usr.username},\nYour OTP is {usr_otp}\nThanks!'

                 send_mail(
                    "welcome to Mina's outfits-Verify your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently=False
                    )
                # print("OTP sent to:", usr.email)
                 return render(request,'signup.html',{'otp':True,'usr':usr})
                else:
                        print(form.errors)
    else:
            form=SignUpForm()
    return render(request,'signup.html',{'form':form})
def resend_otp(request):
	if request.method == "GET":
		get_usr = request.GET['usr']
		if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
			usr = User.objects.get(username=get_usr)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello, {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to MINA's Beuty - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return HttpResponse("Resend")

	return HttpResponse("Can't Send ")


def login_view(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':
		get_otp = request.POST.get('otp')  

		if get_otp:
			get_usr = request.POST.get('usr')
			usr = User.objects.get(username=get_usr)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				login(request, usr)
				return redirect('home')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'login.html', {'otp': True, 'usr': usr})


		usrname = request.POST['username']
		passwd = request.POST['password']

		user = authenticate(request, username = usrname, password = passwd) 
		if user is not None:
			login(request, user)
			return redirect('home')
		elif not User.objects.filter(username = usrname).exists():
			messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
			return redirect('signin')
		elif not User.objects.get(username=usrname).is_active:
			usr = User.objects.get(username=usrname)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to Zena Beauty - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return render(request, 'login.html', {'otp': True, 'usr': usr})
		else:
			messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
			return redirect('signin')

	form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})


def Profile(request):
  if request.user.is_authenticated:
    if profile.objects.filter(user=request.user):
        userprofile = get_object_or_404(profile, user=request.user)
    else:
        userprofile = profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = profileUpdate(request.POST, request.FILES, instance=request.user.profile)
        # pic_form = ProfilePictureUpdate(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid :
            u_form.save()
            p_form.save()
            # pic_form.save()
            messages.success(request, f'updated successfully')
        else:
            messages.error(request, 'There was an error while updating your profile')
    else:
        u_form = UserUpdate(instance=request.user)
        p_form = profileUpdate(instance=request.user.profile)
       
    Cart = cart.objects.filter(user=request.user)
    item_count = Cart.count
  else:
    return redirect('signin')

  return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form,  'userprofile': userprofile, 'item_count': item_count})


