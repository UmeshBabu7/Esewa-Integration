from django.shortcuts import render, redirect
from product.models import *
from .filters import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import LoginForm, OrderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse


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
    # Only filter cart items if user is authenticated
    if user.is_authenticated:
        items=Cart.objects.filter(user=user)
    else:
        items=Cart.objects.none()  # Return empty queryset for anonymous users
    data={
        'product':product,
        'items':items
    }
    return render(request, 'user/homepage.html', data)


def productpage(request):
    user=request.user
    # Only filter cart items if user is authenticated
    if user.is_authenticated:
        items=Cart.objects.filter(user=user)
    else:
        items=Cart.objects.none()  # Return empty queryset for anonymous users
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
            return redirect(reverse('esewaform')+"?o_id="+str(order.id)+"&c_id="+str(cart.id))
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


import hmac #cryptography algorithm
import hashlib #encrypt data
import uuid #to generate random string
import base64

class EsewaView(View):
    def get(self, request, *args, **kwargs):
        o_id=request.GET.get('o_id')
        c_id=request.GET.get('c_id')
        cart=Cart.objects.get(id=c_id)
        order=Order.objects.get(id=o_id)

        uuid_val=uuid.uuid4()

        def genSha256(key, message):
            key=key.encode('utf-8')
            message=message.encode('utf-8')

            hmac_sha256=hmac.new(key,message, hashlib.sha256)

            digest=hmac_sha256.digest()

            signature=base64.b64encode(digest).decode('utf-8')
            return signature
        
        secret_key='8gBm/:&EnhH.1/q'
        data_to_sign=f"total_amount={order.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"

        result=genSha256(secret_key, data_to_sign)

        data={
            'amount':order.product.product_price,  
            'total_amount':order.total_price,
            'transaction_uuid':uuid_val,
            'product_code':'EPAYTEST',
            'signature':result,
        }
        context={
            'order':order,
            'data':data,
            'cart':cart
        }
        return render(request, 'user/esewa_payment.html',context)


import json
@login_required
def esewa_verify(request, order_id, cart_id):
    if request.method =='GET':
        data=request.GET.get('data')
        decoded_data=base64.b64decode(data).decode('utf-8')
        map_data=json.loads(decoded_data)
        order=Order.objects.get(id=order_id)
        cart=Cart.objects.get(id=cart_id)

        if map_data.get('status') == 'COMPLETE':
            order.payment_status = 'completed'
            order.save()
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'Payment Successful')
            return redirect('myorder')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to make a payment')
            return redirect('myorder')



@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        new_email = request.POST.get('email', '').strip()

        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Profile updated successfully')
        return redirect('profile')

    data = {
        'user': user
    }
    return render(request, 'user/profile.html', data)
