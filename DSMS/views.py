from datetime import datetime
from itertools import product
from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Product
from .models import Approvals
from .models import Orders
from .forms import AddProductForm
from .idGenereator import generateId
from django.contrib.auth import get_user_model
import datetime


# Create your views here.
def index(request):
    queryset = Product.objects.all()
    title = 'Developer'
    context = {
        'queryset': queryset,
        'title':title
    }
    return render(request, 'index.html', context)

def dashboard(request):
    user_total = num_of_users()
    approval_total = num_of_approvals()
    order_total = num_of_orders()
    orders = Orders.objects.all()
    context = {
        'orders': orders,
        'user_total':user_total, 
        'approval_total': approval_total,
        'order_total': order_total,
    }
    return render(request, 'dashboard.html', context)

def engineers_page(request):
    queryset = Product.objects.all()
    context = {
        'queryset': queryset 
    }
    
    return render(request, 'home_page.html', context)

def home_order(request):
    orders = Orders.objects.all()
    context = {
        'orders': orders 
    }
    
    return render(request, 'home_order.html', context)

def home_approvals(request):
    username = request.user.username
    orders = Orders.objects.filter(username=username)
    context = {
        'orders': orders, 
    }
    return render(request, 'home_approvals.html', context)

def order_list(request):
    orders = Orders.objects.all()
    context = {
        'orders': orders 
    }
    return render(request, 'orders.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        superusers = User.objects.filter(is_superuser=True)
        if user is not None:
            if username == "admin":
                login(request, user)
                return redirect('dashboard')
            else: 
                login(request, user)
                return redirect('home_page')
        else:
            return redirect('login_page')
    else:
        return render(request, 'pages-login.html')



def page_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect('user_list')
        else:
            messages.info(request, 'Passwords Do Not Match')
            return redirect('page-register')


        
def product_list(request):
    queryset = Product.objects.all()
    context = {
        'queryset': queryset 
    }
    
    return render(request, 'product_view.html', context)


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        category = request.POST['category']
        product_quantity = int(request.POST['product_qty'])
        brand = request.POST['brand']
        product_id = generateId(4)
        
        new_product = Product(product_name=product_name, category=category, product_quantity=product_quantity, brand=brand, product_id=product_id)
        new_product.save()
        messages.success(request, "Product has been added to stock successfully.")
        
        return redirect('product_list')
    
def add_items(request):
	form = AddProductForm(request.POST or None)
	if form.is_valid():
		form.save()
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_product.html", context)


def user_list(request):
    User = get_user_model()
    users = User.objects.all()
    context = {
        'users': users 
    }
    
    
    return render(request, 'users.html', context)

def sign_out(request):
    return redirect('/')

def add_order(request): 
    if request.method == 'POST':
        product_name = request.POST['product_name']
        order_quantity = int(request.POST['product_qty'])
        order_id = generateId(4)
        username = request.user.username
        Date = datetime.date.today()
        product_quantity = Product.product_quantity 
        
        #Checking if ordered quantity is available in stock
        q = Product.objects.get(product_name=product_name)
        product_quantity = q.product_quantity
        if order_quantity <= product_quantity:
            new_order = Orders(product_name=product_name, product_quantity=order_quantity, order_id=order_id, username=username, date=Date, ordered=True)
            new_order.save()
            messages.success(request, "product request sent successfully")
            return redirect('home_page')
        else:
            messages.error(request, "requested quantity not available")
            return redirect('home_page')
            


# order approval
def approve_order(request, order_id):
    product_quantity = Product.product_quantity 
    
    order = Orders.objects.get(id=order_id)
    ordered_quantity = order.product_quantity
    product_ordered_name = order.product_name
    product = Product.objects.get(product_name=product_ordered_name)
    product_qty = product.product_quantity
    product_qty -= ordered_quantity
    order.approved = True
    order.save()
    Product.objects.filter(product_name=product_ordered_name).update(product_quantity=product_qty)
    return redirect('order_list')

# order reject
def reject_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    order.rejected = True
    order.save()
    return redirect('order_list')

def num_of_users():
    users = User.objects.all()
    users_total = 0
    for user in users:
        users_total += 1
    return users_total
 
 #total number of approvals   
def num_of_approvals():
    orders = Orders.objects.all()
    approval_total = 0
    for order in orders:
        if order.approved:
            approval_total += 1
    return approval_total

#Total number of orders
def num_of_orders():
    orders = Orders.objects.all()
    order_total = 0
    for order in orders:
        if order.date == datetime.date.today():
            order_total += 1
            
    return order_total
    
        
 