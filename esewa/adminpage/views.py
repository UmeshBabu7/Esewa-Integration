from django.shortcuts import render, redirect
from product.models import *
from product.forms import *
from django.contrib import messages
from user.auth import *
from django.contrib.auth.decorators import login_required

# Create your views here.

@admin_only
def adminhome(request):
    return render(request, 'adminpage/dashboard.html')

@admin_only
def productlist(request):
    product=Product.objects.all()
    # messages.add_message(request, messages.SUCCESS, 'Added product successfully in a cart')
    return render(request, 'adminpage/productlist.html', {'product':product})

@login_required
@admin_only
def addproduct(request):
    if request.method == 'POST':
        form=ProductForm(request.POST, request.FILES)
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
@admin_only
def categorylist(request):
    category=Category.objects.all()
    return render(request, 'adminpage/categorylist.html', {'category':category})

@admin_only
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


# update and delete product
def updateproduct(request, product_id):
    instance=Product.objects.get(id=product_id)
    if request.method == 'POST':
        form=ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product updated successfully !')
            return redirect('productlist')
        else:
            messages.add_message(request, messages.ERROR, 'Error occurr while updating product !')
            return render(request, 'adminpage/updateproduct.html', {'form':form})
    forms={
        'form':ProductForm(instance=instance)
    }
    return render(request, 'adminpage/updateproduct.html', forms)


def deleteproduct(request, product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    messages.add_message(request, messages.SUCCESS, 'Product deleted successfully !')
    return redirect('productlist')



# update and delete category
def updatecategory(request, category_id):
    instance=Category.objects.get(id=category_id)
    if request.method == 'POST':
        form=CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category updated successfully !')
            return redirect('categorylist')
        else:
            messages.add_message(request, messages.ERROR, 'Error occurr while updating category !')
            return render(request, 'adminpage/updatecategory.html', {'form':form})
    forms={
        'form':CategoryForm(instance=instance)
    }
    return render(request, 'adminpage/updatecategory.html', forms)


def deletecategory(request, category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, 'Category deleted successfully !')
    return redirect('categorylist')