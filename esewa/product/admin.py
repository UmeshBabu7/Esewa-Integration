from django.contrib import admin
from .models import Category, Product, Cart, Order

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name','created_at']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display=['id','product_name','product_price','description','quantity','image','category']

admin.site.register(Product, ProductAdmin)

admin.site.register(Cart)


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'user',
        'total_price',
        'quantity',
        'payment_method',
        'payment_status',
        'contact_no',
        'address',
        'email',
    ]
    list_filter = ['payment_method', 'payment_status']
    search_fields = ['product__product_name', 'user__username', 'email', 'address', 'contact_no']
    list_select_related = ['product', 'user']


admin.site.register(Order, OrderAdmin)