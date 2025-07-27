from django.shortcuts import render
from product.models import *

# Create your views here.

def adminhome(request):
    return render(request, 'adminpage/dashboard.html')

def productlist(request):
    product=Product.objects.all()
    return render(request, 'adminpage/productlist.html', {'product':product})