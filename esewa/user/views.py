from django.shortcuts import render, redirect
from product.models import *
from .filters import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'User account has been created successfully !')
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Please provide correct credential !')
    else:
        form=UserCreationForm()
    return render(request, 'user/register.html', {'form':form})


def login_user(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request, username=data['username'], password=data['password']) # read data

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
               messages.add_message(request, messages.ERROR, 'Please provide correct credential !')
    else:
        form=LoginForm()
    return render(request, 'user/login.html', {'form':form})

def logout_user(request):
    logout(request)
    return redirect('login')


def homepage(request):
    product=Product.objects.all().order_by('-id')[:4]
    data={
        'product':product
    }
    return render(request, 'user/homepage.html', data)


def productpage(request):
    product=Product.objects.all()
    product_filter=ProductFilter(request.GET, queryset=product)
    product_final=product_filter.qs
    data={
        'product':product_final,
        'product_filter':product_filter
    }
    return render(request, 'user/productpage.html', data)

def productdetail(request, product_id):
    product=Product.objects.get(id=product_id)
    data={
        'product':product
    }
    return render(request, 'user/productdetail.html', data)