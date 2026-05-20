from django.shortcuts import render, redirect
from product.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


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