from enum import auto
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User,auth
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
import datetime

from django.http import JsonResponse
import json

# Create your views here.
def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_item
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store.html', context)

# @login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
     customer = request.user.customer
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     items = order.orderitem_set.all()
     cartItems = order.get_cart_item
    else:
     #Create empty cart for now for non-logged in user
     items = []
     order={'get_cart_total':0,'get_cart_item':0,'shipping':False}   
    
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',context)


# def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid') 
            return redirect('/login/')
    else:
      return render(request,'login.html')


# def signup(request):
    
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('/signup/')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                
                #cree un neveau profile
                user_model=User.objects.get(username=username)
                new_profile=Customer.objects.create(user=user_model)
                new_profile.save()
                return redirect("/")
        else:
             messages.info(request,'Password not matching')
             return redirect('/signup/')   
    else:
        return render(request,'signup.html')
    
# @login_required(login_url='login')
def main(request):
 if request.user.is_authenticated:
  customer = request.user.customer
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  items = order.orderitem_set.all()
  cartItems = order.get_cart_item
 else:
  items = []
  order = {'get_cart_total':0, 'get_cart_items':0}
  cartItems = order['get_cart_items']
 context = {'cartItems':cartItems}
 return render(request, 'store.html', context)


# @login_required(login_url='login')
def cart(request):
 if request.user.is_authenticated:
  customer = request.user.customer
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  items = order.orderitem_set.all()
  cartItem=order.get_cart_item
 else:
  #Create empty cart for now for non-logged in user
  items = [] 
 
 context = {'items':items,'order':order,'cartItem':cartItem}
 return render(request, 'cart.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
 transaction_id = datetime.datetime.now().timestamp()
 data = json.loads(request.body)  
 if request.user.is_authenticated:
   customer = request.user.customer
   order, created = Order.objects.get_or_create(customer=customer, complete=False)
   total = float(data['form']['total'])
   order.transaction_id = transaction_id
   if total == order.get_cart_total:
      order.complete = True
   order.save()
   if order.shipping==True:
       ShippingAddress.objects.create(
           customer=customer,
           order=order,
           address=data['shipping']['address'],
           city=data['shipping']['state'],
           zipcode=data['shipping']['zipcode']
       )
 else:
   print('User is not logged in')  
 return JsonResponse('Payment submitted..', safe=False)
