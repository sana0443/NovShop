from django.urls import path,include
from .import views 
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView



urlpatterns = [
    path('signin/',views.Signin,name='signin'),
    path('logout/',views.logoutuser,name="logout"),
    path('signup/',views.signup,name="signup"),
   
	


]
