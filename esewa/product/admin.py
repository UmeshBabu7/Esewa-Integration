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
admin.site.register(Order)