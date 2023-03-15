from.import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('category/<int:id>',views.CategoryView.as_view(),name='category'),
    # path('category-title/<val>',views.CategoryView.as_view(),name='category-title'),
    path('product-details/<int:pk>',views.product_details.as_view(),name="product-details"),
    path('add-to-cart/<int:prod_id>',views.add_to_cart,name='add-to-cart'),
    # path('shop-cart/',views.cart,name='shop-cart'),
    path('cart/',views.show_cart,name='show-cart'),
    # path('shop/',views.shop,name='shop'),
    path('remove_cart_item/<int:cart_id>/',views.remove_cart_item, name='remove_cart_item'),
    path('filter-by-size/', views.filter_by_size, name='filter_by_size'),
    path('products/<int:pid>',views.products,name='products'),
    path('search/', views.search, name='search'),
    # path('checkout/',views.checkout,name='checkout'),
    path('place_order/',views.place_order,name='place_order'),
    path('proceed-to-pay/',views.razor_pay,name='proceed-to-pay'),
    path('product_filter/',views.product_filter,name='filter'),
    # path('add_cart_icon/<int:prod_id>',views.add_cart_icon,name='carticon'),
    path('wishlist/<int:pk>',views.wishlist,name='wishlist'),
    path('wishlist_view/',views.Wishlist_View,name='wishlists'),
    path('coupen/',views.coupon,name='coupen'),
    path('orders/',views.orders,name='orders'),
    path('view_orders/<str:t_no>',views.view_orders,name='view_orders'),
     path('view_product_order/<str:trackno>',views.view_product_order,name='view_product_order'),
    path('cancel_order/<str:order_id>',views.cancel_order,name='cancel_order'),
    path('wallet_balance/', views.wallet_balance, name='wallet_balance'),
    path('remove_wishlist/<int:pk>',views.remove_wishlist,name='remove_wishlist')


    

    # path('some-error-page/', views.error_view, name='error_page'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
