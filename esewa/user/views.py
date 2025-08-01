from django.shortcuts import render
from product.models import *

# Create your views here.

def homepage(request):
    product=Product.objects.all().order_by('-id')[:4]
    data={
        'product':product
    }
    return render(request, 'user/homepage.html', data)


def productpage(request):
    product=Product.objects.all()
    data={
        'product':product
    }
    return render(request, 'user/productpage.html', data)