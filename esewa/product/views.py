from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Product

# Create your views here.


def product(request):
    return HttpResponse("product page")

def home(request):
    product=Product.objects.all()
    items={
        'product':product
    }
    return render(request, 'product/index.html', items)


def productpage(request):
    return render(request, 'product/productpage.html')