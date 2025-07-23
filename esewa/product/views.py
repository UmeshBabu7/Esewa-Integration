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
    return render(request, 'index.html', items)