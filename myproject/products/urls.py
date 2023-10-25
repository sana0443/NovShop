from.import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('category/<int:id>',views.CategoryView.as_view(),name='category'),
    path('add-to-cart/<int:prod_id>',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='show-cart'),
    path('products/<int:pid>',views.products,name='products'),
    path('products/',views.products,name='products'),
    path('remove_cart_item/<int:cart_id>/',views.remove_cart_item, name='remove_cart_item'),
     

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
