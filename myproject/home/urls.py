from django.urls import path,include
from .import views 
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView



urlpatterns = [
    path('signin/',views.Signin,name='signin'),
    # path('home/',views.home,name='home'),
    # path('',views.home2,name='home2'),
    path('profile/',views.Profile,name='profile'),
    path('logout/',views.logoutuser,name="logout"),
    path('signup/',views.signup,name="signup"),
   
    path("password-reset/", 
    	PasswordResetView.as_view(template_name='password_reset.html'),
    	name="password_reset"),

	path("password-reset/done/", 
		PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
		name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/", 
		PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
		name="password_reset_confirm"),

	path("password-reset-complete/", 
		PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
		name="password_reset_complete"),

	path('resendOTP',views.resend_otp),
	# path('send-promotional-email/',views.send_promotional_email, name='send_promotional_email'),


]
