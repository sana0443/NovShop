from django.contrib import admin
from .models import product, cart, Category,Address


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discount_price', 'category', 'product_image']

class cartModelAdmin(admin.ModelAdmin):
    list_display=['id','product','quantity']



admin.site.register(product, ProductModelAdmin)
admin.site.register(cart,cartModelAdmin)
admin.site.register(Category)
admin.site.register(Address)

# admin.site.register(variation,variationModelAdmin)


