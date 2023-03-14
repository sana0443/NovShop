from django.contrib import admin
from .models import product, cart, Category,Address,Order,OrderItem,variation,coupen,Refund,Wallet


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discount_price', 'category', 'product_image']

class cartModelAdmin(admin.ModelAdmin):
    list_display=['id','product','quantity']

class variationModelAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'variation_category', 'variation_value', 'is_active']
    list_editable=['is_active',]
    list_filter=['product','variation_category','variation_value']

    def get_category(self, obj):
        return obj.category.name if obj.category else ''
    get_category.short_description = 'Category'

admin.site.register(product, ProductModelAdmin)
admin.site.register(cart,cartModelAdmin)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(variation,variationModelAdmin)
admin.site.register(coupen)
admin.site.register(Refund)
admin.site.register(Wallet)

