from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, Buyer, Product, Order
from .forms import SupplierForm, BuyerForm, ProductForm, OrderForm,SupplierProductForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerRegistrationForm, BuyerRegistrationForm, SellerLoginForm, BuyerLoginForm,AddOrderForm
from django.core.mail import send_mail
from django.conf import settings
import requests






from django.contrib.auth import authenticate
from django.http import JsonResponse
import requests

def api_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # API সার্ভারে লগিন রিকোয়েস্ট পাঠানো
        response = requests.post(
            'http://127.0.0.1:8000/api/token/',
            data={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            # টোকেন সেশন বা কুকিতে স্টোর করুন
            request.session['access_token'] = response.json().get('access')
            request.session['refresh_token'] = response.json().get('refresh')
            return redirect('dashboard')
        else:
            return render(request, '/accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, '/accounts/login.html')






def home(request):
    return render(request, 'index.html')




@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')
from django.shortcuts import render, redirect
from .models import Supplier, Buyer, Product, Order
from .forms import SupplierForm, BuyerForm, ProductForm, OrderForm
@login_required
def dashboard(request):
    suppliers = Supplier.objects.count()
    buyers = Buyer.objects.count()
    products = Product.objects.count()
    orders = Order.objects.count()
    context = {
        'suppliers': suppliers,
        'buyers': buyers,
        'products': products,
        'orders': orders,
        'orders_list': Order.objects.all().select_related('buyer', 'product')[:10]
    }
    return render(request, 'dashboard.html', context)
"""def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})"""


def supplier_list(request):
    headers = {
        'Authorization': f'Bearer {request.session.get("access")}'
    }
    
    try:
        response = requests.get(
            'http://127.0.0.1:8000/api/suppliers/',
            headers=headers
        )
        
        if response.status_code == 200:
            return render(request, 'supplier_list.html', {'suppliers': response.json()})
        elif response.status_code == 401:  # টোকেন এক্সপায়ার্ড
            return redirect('refresh-token')
    except requests.exceptions.RequestException:
        return render(request, 'error.html')
"""
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier_form.html', {'form': form})"""


def supplier_add(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'contact': request.POST.get('contact'),
            'email': request.POST.get('email'),
        }
        # API তে POST request পাঠান
        response = requests.post('http://127.0.0.1:8000/api/suppliers/', data=data)
        if response.status_code == 201:  # 201 মানে Created (সফলভাবে তৈরি হয়েছে)
            return redirect('supplier_list')
    return render(request, 'supplier_form.html')
def supplier_edit(request, pk):
    supplier = Supplier.objects.get(pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_form.html', {'form': form})


def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})


# Buyer CRUD
"""def buyer_list(request):
    buyers = Buyer.objects.all()
    return render(request, 'buyer_list.html', {'buyers': buyers})"""
def buyer_list(request):
    response = requests.get('http://127.0.0.1:8000/api/buyers/')
    buyers = response.json()
    return render(request, 'buyer_list.html', {'buyers': buyers})
def buyer_create(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buyer_list')
    else:
        form = BuyerForm()
    return render(request, 'buyer_form.html', {'form': form})

def buyer_update(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    if request.method == 'POST':
        form = BuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect('buyer_list')
    else:
        form = BuyerForm(instance=buyer)
    return render(request, 'buyer_form.html', {'form': form})

def buyer_delete(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    if request.method == 'POST':
        buyer.delete()
        return redirect('buyer_list')
    return render(request, 'buyer_confirm_delete.html', {'buyer': buyer})

# Product CRUD
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})



def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

# Order CRUD
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'order_confirm_delete.html', {'order': order})



# dashboard/views.py

# Seller Register
def seller_register(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Wait for admin approval.')
            return redirect('seller_login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'seller_register.html', {'form': form})

# Buyer Register
def buyer_register(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Wait for admin approval.')
            return redirect('buyer_login')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'buyer_register.html', {'form': form})

# Seller Login
def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                seller = Supplier.objects.get(email=email)
                if not seller.is_approved:
                    messages.error(request, 'Your account is not approved yet.')
                elif seller.password == password:
                    request.session['seller_id'] = seller.id
                    return redirect('seller_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except Supplier.DoesNotExist:
                messages.error(request, 'Seller does not exist.')
    else:
        form = SellerLoginForm()
    return render(request, 'seller_login.html', {'form': form})

# Buyer Login
def buyer_login(request):
    if request.method == 'POST':
        form = BuyerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                buyer = Buyer.objects.get(email=email)
                if not buyer.is_approved:
                    messages.error(request, 'Your account is not approved yet.')
                elif buyer.password == password:
                    request.session['buyer_id'] = buyer.id
                    return redirect('buyer_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except Buyer.DoesNotExist:
                messages.error(request, 'Buyer does not exist.')
    else:
        form = BuyerLoginForm()
        messages.error(request,'ki hocche bujhtesi na')
    return render(request, 'buyer_login.html', {'form': form})

# Pending Users List (Admin Panel)
def pending_users(request):
    sellers = Supplier.objects.filter(is_approved=False)
    buyers = Buyer.objects.filter(is_approved=False)
    return render(request, 'pending_users.html', {'sellers': sellers, 'buyers': buyers})

# Approve user by admin
from .utils import send_approval_email
def approve_user(request, user_type, user_id):
    if user_type == 'seller':
        user = Supplier.objects.get(id=user_id)
    elif user_type == 'buyer':
        user = Buyer.objects.get(id=user_id)
    else:
        user = None

    if user:
        user.is_approved = True
        user.save()
        # Send email
        send_approval_email(user)  # call the mail sender
    messages.success(request, f'{user.name} has been approved and email sent.')

    return redirect('pending_users')

"""

def buyer_dashboard(request):
    orders = Order.objects.filter(buyer=request.user)
    return render(request, 'buyer_dashboard.html', {'orders': orders})
"""
def buyer_dashboard(request):
    buyer_id = request.session.get('buyer_id')
    if not buyer_id:
        messages.error(request, 'Please log in first.')
        return redirect('buyer_login')
    
    try:
        buyer = Buyer.objects.get(id=buyer_id)
    except Buyer.DoesNotExist:
        messages.error(request, 'Buyer not found.')
        return redirect('buyer_login')

    orders = Order.objects.filter(buyer=buyer)
    return render(request, 'buyer_dashboard.html', {'orders': orders, 'buyer': buyer})

"""
def seller_dashboard(request):
    supplier_email = request.user.email
    supplier = Supplier.objects.get(email=supplier_email)
    products = Product.objects.filter(supplier=supplier)
    orders = Order.objects.filter(product__supplier=request.user)
    return render(request, 'seller_dashboard.html', {'products': products, 'orders': orders})

    """
def seller_dashboard(request):
    seller_id = request.session.get('seller_id')
    if not seller_id:
        return redirect('seller_login')
    
    supplier = Supplier.objects.get(id=seller_id)
    products = Product.objects.filter(supplier=supplier)
    orders = Order.objects.filter(product__supplier=supplier)
    return render(request, 'seller_dashboard.html', {'products': products, 'orders': orders})


def add_product(request):
    if request.method == 'POST':
        form = SupplierProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier_id = request.session.get('seller_id')
            product.save()
            return redirect('seller_dashboard')
    else:
        form = SupplierProductForm()
    return render(request, 'product_form_seller.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = SupplierProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = SupplierProductForm(instance=product)
    return render(request, 'product_form_seller.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('seller_dashboard')



def add_order(request):
    buyer_id = request.session.get('buyer_id')
    if not buyer_id:
        messages.error(request, 'Please log in first.')
        return redirect('buyer_login')

    buyer = Buyer.objects.get(id=buyer_id)

    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            Order.objects.create(buyer=buyer, product=product, quantity=quantity)
            messages.success(request, 'Order added successfully.')
            return redirect('buyer_dashboard')
    else:
        form = AddOrderForm()

    return render(request, 'add_order.html', {'form': form})


def cancel_order(request, order_id):
    buyer_id = request.session.get('buyer_id')
    if not buyer_id:
        messages.error(request, 'Please log in first.')
        return redirect('buyer_login')
    
    order = get_object_or_404(Order, id=order_id, buyer_id=buyer_id)
    order.delete()
    messages.success(request, 'Order cancelled successfully.')
    return redirect('buyer_dashboard')




def delete_user(request, user_type, user_id):
    if user_type == 'seller':
        user = get_object_or_404(Supplier, id=user_id)
    else:
        user = get_object_or_404(Buyer, id=user_id)
    
    if request.method == 'GET':
        user.delete()
        return redirect('pending_users')  # Redirect back to approvals page
    
    return redirect('pending_users')