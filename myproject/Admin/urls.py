from django.contrib import admin
from django.urls import path
# from Admin.views import *
from django.conf import settings
from . import views

from django.conf.urls.static import static

urlpatterns = [

path('admin-login/', views.adminLogin, name="admin_login"),
path('admin-home/',views.adminHome,name="admin_home"),
path('admin-dsbd/',views.admin_dashboard,name="admin_dsbd"),
path('add-category/', views.add_category, name="add_category"),
path('view-category/', views.view_category, name="view_category"),
path('add-product',views.add_product,name="add_product"),
path('view-product',views.view_product,name="view_product"),
path('edit-category/<int:pid', views.edit_category, name="edit_category"),
path('delete-category/<int:pid>/',views.delete_category, name="delete_category"),
# path('search_products/',views.search_products,name='search_prodcuts'),
path('edit-product/<int:pid>',views.edit_product,name='editproduct'),
path('delete-product/<int:pid>/',views.delete_product, name="delete_product"),
path('order_manage/',views.manage_order,name='order_manage'),
path('admin_view_order/<str:trackno>',views.admin_view_order,name='admin_view_order'),
path('order_shipping/<str:trackno>',views.order_shipping,name='order_shipping'),
path('order_delivared/<str:trackno>',views.order_delivered,name='order_delivered'),
path('order_shipped/<str:trackno>',views.order_shipped,name='order_shipped'),
path('manage_user/',views.manage_user,name='manage_user'),
path('ban_user/<int:user_id>',views.block_user,name='ban_user'),
path('unban_user/<int:user_id>',views.unblock_user,name='unban_user'),

# path('order_chart/', views.OrderChartView.as_view(), name='order_chart'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)