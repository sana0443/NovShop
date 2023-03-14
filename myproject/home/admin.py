from django.contrib import admin
# from.models import signup

from.models import UserOTP,profile
# Register your models here.



admin.site.register(UserOTP)
admin.site.register(profile)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'first_name','last_name', 'email', 'password')


