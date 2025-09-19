from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=200, unique=True)
    created_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name=models.CharField(max_length=200)
    product_price=models.IntegerField()
    description=models.TextField()
    quantity=models.IntegerField()
    image=models.URLField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.product_name
    

class Cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    PAYMENT_METHOD=(
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Esewa', 'Esewa'),
        ('Khalti', 'Khalti')
    )
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price=models.IntegerField()
    quantity=models.IntegerField()
    payment_method=models.CharField(choices=PAYMENT_METHOD, max_length=200)
    payment_status=models.CharField(default='pending', max_length=200)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    contact_no=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    email=models.EmailField()
    
    


    
