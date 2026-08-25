from decimal import Decimal
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product,Order,OrderItem
from .forms import RegisterForm

def home(request):
    return render(request,'store/home.html',{'products':Product.objects.all().order_by('-created_at')})

def product_detail(request,pk):
    return render(request,'store/product_detail.html',{'product':get_object_or_404(Product,pk=pk)})

def _cart(request):
    return request.session.setdefault('cart',{})

def cart_view(request):
    cart=_cart(request); items=[]; total=Decimal('0')
    for key,qty in cart.items():
        try:
            p=Product.objects.get(pk=key)
            subtotal=p.price*qty; total+=subtotal
            items.append({'product':p,'quantity':qty,'subtotal':subtotal})
        except Product.DoesNotExist: pass
    return render(request,'store/cart.html',{'items':items,'total':total})

def add_to_cart(request,pk):
    if request.method=='POST':
        cart=_cart(request); key=str(pk); qty=max(1,int(request.POST.get('quantity',1)))
        cart[key]=cart.get(key,0)+qty; request.session.modified=True
        messages.success(request,'Product added to cart.')
    return redirect('cart')

def update_cart(request,pk):
    if request.method=='POST':
        cart=_cart(request); qty=int(request.POST.get('quantity',1))
        key=str(pk)
        if qty>0: cart[key]=qty
        else: cart.pop(key,None)
        request.session.modified=True
    return redirect('cart')

def remove_from_cart(request,pk):
    cart=_cart(request); cart.pop(str(pk),None); request.session.modified=True
    return redirect('cart')

def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False); user.set_password(form.cleaned_data['password']); user.save()
            login(request,user); messages.success(request,'Account created successfully.')
            return redirect('home')
    else: form=RegisterForm()
    return render(request,'store/register.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        user=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if user: login(request,user); return redirect('home')
        messages.error(request,'Invalid username or password.')
    return render(request,'store/login.html')

def logout_view(request):
    logout(request); return redirect('home')

@login_required
def checkout(request):
    cart=_cart(request)
    if not cart:
        messages.error(request,'Your cart is empty.'); return redirect('home')
    rows=[]; total=Decimal('0')
    for key,qty in cart.items():
        p=get_object_or_404(Product,pk=key)
        if p.stock<qty: messages.error(request,f'Not enough stock for {p.name}.'); return redirect('cart')
        rows.append((p,qty)); total+=p.price*qty
    if request.method=='POST':
        order=Order.objects.create(user=request.user,full_name=request.POST['full_name'],email=request.POST['email'],address=request.POST['address'],total_price=total)
        for p,qty in rows:
            OrderItem.objects.create(order=order,product=p,quantity=qty,price=p.price)
            p.stock-=qty; p.save()
        request.session['cart']={}; request.session.modified=True
        return render(request,'store/order_success.html',{'order':order})
    return render(request,'store/checkout.html',{'total':total})
