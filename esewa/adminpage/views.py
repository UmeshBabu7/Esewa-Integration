from django.shortcuts import render, redirect
from product.models import *
from product.forms import *
from django.contrib import messages

# Create your views here.

def adminhome(request):
    return render(request, 'adminpage/dashboard.html')

def productlist(request):
    product=Product.objects.all()
    return render(request, 'adminpage/productlist.html', {'product':product})


def addproduct(request):
    if request.method == 'POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product has been added successfully !')
            return redirect('addproduct')
        else:
            messages.add_message(request, messages.ERROR, 'Error occure while adding product !')
    else:
        form=ProductForm()
    return render(request, 'adminpage/addproduct.html', {'form':form})


# Category
def categorylist(request):
    category=Category.objects.all()
    return render(request, 'adminpage/categorylist.html', {'category':category})

def addcategory(request):
    if request.method == 'POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ' Category has been added successfully !')
            return redirect('addcategory')
        else:
            messages.add_message(request, messages.ERROR, 'Error occure while adding category !')
    else:
        form=CategoryForm()
    return render(request, 'adminpage/addcategory.html', {'form':form})