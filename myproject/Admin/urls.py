from django.contrib import admin
from django.urls import path
# from Admin.views import *
from django.conf import settings
from . import views

from django.conf.urls.static import static

urlpatterns = [

path('admin-login/', views.adminLogin, name="admin_login"),
path('add-product',views.add_product,name="add_product"),
path('edit-product/<int:pid>',views.edit_product,name='editproduct'),
path('view-product',views.view_product,name="view_product"),
path('delete-product/<int:pid>/',views.delete_product, name="delete_product"),
path('add-category/', views.add_category, name="add_category"),
path('admin_logout/',views.logoutadmin,name='admin_logout')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)