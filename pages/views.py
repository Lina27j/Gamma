from django.shortcuts import render, redirect
from product.models import Product, Quotation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Client.models import Client
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.prefetch_related('image').all()[:6]
    print(products)
    return render(request, 'home.html', {'products': products})


def login_view(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = True
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/')



def signup_view(request):
    error = None
    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('/')

    return render(request, 'signup.html', {'error': error})

@login_required(login_url='/login/')
def dashboard(request):
    client = Client.objects.filter(user=request.user).first()
    quotations = Quotation.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'dashboard.html', {
        'client': client,
        'quotations': quotations,
    })

def about(request):
    return render(request, 'about.html')
