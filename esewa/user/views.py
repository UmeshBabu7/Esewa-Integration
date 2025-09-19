from django.shortcuts import render, redirect
from product.models import *
from .filters import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import LoginForm, OrderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
                if user.is_staff:
                    return redirect('admins')
                else:
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
    user=request.user
    product=Product.objects.all().order_by('-id')[:4]
    items=Cart.objects.filter(user=user)
    data={
        'product':product,
        'items':items
    }
    return render(request, 'user/homepage.html', data)


def productpage(request):
    user=request.user
    items=Cart.objects.filter(user=user)
    product=Product.objects.all()
    # For Filter Product
    product_filter=ProductFilter(request.GET, queryset=product)
    product_final=product_filter.qs
    data={
        'product':product_final,
        'product_filter':product_filter,
        'items':items
    }
    return render(request, 'user/productpage.html', data)

def productdetail(request, product_id):
    product=Product.objects.get(id=product_id)
    data={
        'product':product
    }
    return render(request, 'user/productdetail.html', data)


@login_required
def add_to_cart(request, product_id):
    user=request.user
    product=Product.objects.get(id=product_id)

    check_items=Cart.objects.filter(user=user, product=product)
    if check_items:
        messages.add_message(request, messages.ERROR, 'Product is already added in a cart')
        return redirect('productpage')
    else:
        Cart.objects.create(user=user, product=product)
        messages.add_message(request, messages.SUCCESS, 'Added product successfully in a cart')
        return redirect('cartlist')


@login_required
def cart_list(request):
    user=request.user
    items=Cart.objects.filter(user=user)
    data={
        'items':items
    }
    return render(request, 'user/cart.html', data)


@login_required
def orderitem(request, product_id, cart_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    cart=Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form=OrderForm(request.POST)
        quantity=request.POST.get('quantity')
        price=product.product_price
        total_price=int(quantity)*int(price)
        contact_no=request.POST.get('contact_no')
        address=request.POST.get('address')
        email=request.POST.get('email')
        payment_method=request.POST.get('payment_method')

        order=Order.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            contact_no=contact_no,
            address=address,
            email=email,
            payment_method=payment_method,
        )

        if order.payment_method == 'Cash on Delivery':
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'Order has been successfully. Be ready with cash')
            return redirect('cartlist')
        elif order.payment_method == 'Esewa':
            pass
        elif order.payment_method == 'Khalti':
            pass
        else:
            messages.add_message(request, messages.ERROR, 'Invalid payment options')
            return redirect('cartlist')
        
    form={
        'form':OrderForm
    }
    return render(request, 'user/orderform.html', form)


@login_required
def orderlist(request):
    user=request.user
    order=Order.objects.filter(user=user)
    data={
        'order':order
    }
    return render(request, 'user/myorder.html', data)