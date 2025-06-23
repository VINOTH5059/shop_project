from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from shop.form import CustomerUserForm
from django.contrib.auth import  authenticate,login,logout
import json

def Home(request):
    products=Product.objects.filter(status=0) 
    return render(request,'shop/home.html',{"products":products})

def card_page(request):
    if request.user.is_authenticated:
        carts = cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": carts})
    else:
        return redirect('login')

def remove_from_cart(request, cart_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(cart, id=cart_id, user=request.user)
        cart_item.delete()
    return redirect('cart_page')  # Use your cart view's URL name
    
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = int(data['product_qty'])
            product_id = int(data['pid'])

            product = Product.objects.get(id=product_id)

            # Check if already in cart
            if cart.objects.filter(user=request.user, product=product).exists():
                return JsonResponse({'status': 'Product already in cart'}, status=200)
            else:
                cart.objects.create(
                    user=request.user,
                    product=product,
                    product_qty=product_qty
                )
                return JsonResponse({'status': 'Product added to cart successfully!'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    return JsonResponse({'status': 'Invalid Access'}, status=400)
def Register(request):
    form=CustomerUserForm()
    if request.method=='POST':
        form=CustomerUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Register Success you can Log in Now")
            return redirect('/login')
    return render(request,'shop/register.html' ,{'form':form})
def login_page(request):
    if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully")
            redirect('/')
        else:
            messages.error(request,"invalid User Name or Password")
            return redirect('/login')
    return render(request,'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect("/")
def category(request):
    categorys=Category.objects.filter(status=0)
    return render(request,'shop/category.html',{"categorys":categorys})
def product(request):
    products=Product.objects.filter(status=0)   
    return render(request,'shop/product.html',{"products":products})
def productDetails(request, id):
    try:
        product_detail = Product.objects.get(id=id, status=0)
        return render(request, 'shop/product_details.html', {"products_details": product_detail})
    except Product.DoesNotExist:
        messages.error(request, "No such product found")
        return redirect('product')

# def productDetails(request, id):
#     try:
#         product_detail = Product.objects.get(id=id, status=0)
#     except Product.DoesNotExist:
#         messages.error(request, "No such product found")
#         return redirect('product')
#     return render(request, 'shop/product_details.html', {"products_details": product_detail})

# def productDetails(request, pname):
#     if Product.objects.filter(name=pname, status=0).exists():
#         product_detail = Product.objects.get(name=pname, status=0)
#         return render(request, 'shop/product_details.html', {"products_details": product_detail})
#     else:
#         messages.error(request, "No such product found")
#         return redirect('product')
