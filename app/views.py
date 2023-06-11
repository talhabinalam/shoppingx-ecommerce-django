from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, ProfileFrom
from django.contrib import messages
from django.db.models import Q, F
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Home(View):
    def get(self, request):
        total_item = 0
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, 'total_item':total_item})

class ProductDetails(View):
    def get(self, request, pk):
        total_item = 0
        product = Product.objects.get(pk=pk)
        item_in_cart = False
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
            item_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_in_cart': item_in_cart, 'total_item':total_item})


@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):
        total_item = 0
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        form = ProfileFrom()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'total_item': total_item})
    
    def post(self, request):
        form = ProfileFrom(request.POST)
        total_item = 0
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            district = form.cleaned_data['district']
            data = Customer(user=user, name=name, location=location, city=city, zipcode=zipcode, district=district)
            data.save()
            messages.success(request, "Congratulations! Profile updated successfully.")
            if request.user.is_authenticated:
                total_item = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'total_item': total_item})


def address(request):
    add = Customer.objects.filter(user=request.user)
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'total_item': total_item})


def mobile(request, data=None):
    total_item = 0
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Xiaomi' or data == 'Samsung' or data == 'Realme':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discount_price__gt=500) #field lookups
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discount_price__lt=500)
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'total_item': total_item})


def laptop(request, data=None):
    total_item = 0
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'HP' or data == 'Acer' or data == 'Dell':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html', {'laptops':laptops, 'total_item': total_item})


def topwear(request):
    total_item = 0
    topwears = Product.objects.filter(category='TW')
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html', {'topwears':topwears, 'total_item': total_item})


def bottomwear(request):
    total_item = 0
    bottomwears = Product.objects.filter(category='BW')
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears, 'total_item': total_item})


class CustomerRegistration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Registered Successfully.")
        return render(request, 'app/customerregistration.html', {'form':form})
    
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('pro_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart/')


@login_required
def show_cart(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amound = 15.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discount_price)
                amount += temp_amount
                total_amount = amount + shipping_amound
            context = {
                'carts':cart, 
                'amount':amount, 
                'total_amount': total_amount, 
                'shipping_amound': shipping_amound,
                'total_item': total_item
                }
            return render(request, 'app/addtocart.html', context)
        else:
            return render(request, 'app/emptycart.html', {'total_item': total_item})


@login_required
def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        pro_id = request.GET['pro_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 15.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        pro_id = request.GET['pro_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 15.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method == 'GET':
        user = request.user
        pro_id = request.GET['pro_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=user))
        c.delete()
        amount = 0.0
        shipping_amount = 15.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)
    
    
def search_results(request):
    query = request.GET.get('q')
    total_item = 0
    if not query:
        return redirect('/')
    products = Product.objects.filter(title__icontains=query)
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    context = {
        'query': query,
        'products': products,
        'total_item': total_item
    }
    return render(request, 'app/search_results.html', context)


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user).annotate(total_cost=F('quantity') * F('product__discount_price'))
    total_item = 0
    amount = 0.0
    shipping_amount = 15.0
    total_amount = 0.0
    cart_product = [p for p in cart_items if p.user == user]
    if cart_product:
        for p in cart_product:
            temp_amount = p.total_cost
            amount += temp_amount
        total_amount = amount + shipping_amount
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items, 'amount': amount, 'shipping_amount':shipping_amount, 'total_item':total_item})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'op':op, 'total_item':total_item})
