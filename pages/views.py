from django.shortcuts import render, redirect
from product.models import Product, Quotation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Client.models import Client
from django.contrib.auth.decorators import login_required
from company.models import CompanyProfile, ContactMessage


def home(request):
    products = Product.objects.prefetch_related('image').all()[:6]
    company  = CompanyProfile.objects.first()
    return render(request, 'home.html', {'products': products, 'company': company})


def login_view(request):
    error   = False
    company = CompanyProfile.objects.first()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = True
    return render(request, 'login.html', {'error': error, 'company': company})


def logout_view(request):
    logout(request)
    return redirect('/')



def signup_view(request):
    error   = None
    company = CompanyProfile.objects.first()
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

            Client.objects.create(
                user      = user,
                firstName = '',
                lastName  = '',
                company   = '',
                phoneNum  = '',
                email     = email,
            )

            login(request, user)
            return redirect('/')

    return render(request, 'signup.html', {'error': error, 'company': company})

@login_required(login_url='/login/')
def dashboard(request):
    client     = Client.objects.filter(user=request.user).first()
    quotations = Quotation.objects.filter(user=request.user).prefetch_related('items__product').order_by('-submitted_at')
    company    = CompanyProfile.objects.first()
    return render(request, 'dashboard.html', {
        'client'    : client,
        'quotations': quotations,
        'company'   : company,
    })


@login_required(login_url='/login/')
def update_profile(request):
    client  = Client.objects.filter(user=request.user).first()
    success = False
    company = CompanyProfile.objects.first()

    if request.method == 'POST':
        first_name   = request.POST.get('first_name', '')
        last_name    = request.POST.get('last_name', '')
        company_name = request.POST.get('company', '')
        phone        = request.POST.get('phone', '')
        email        = request.POST.get('email', '')

        if client:
            client.firstName = first_name
            client.lastName  = last_name
            client.company   = company_name
            client.phoneNum  = phone
            client.email     = email
            client.save()
        else:
            client = Client.objects.create(
                user      = request.user,
                firstName = first_name,
                lastName  = last_name,
                company   = company_name,
                phoneNum  = phone,
                email     = email,
            )

        request.user.email = email
        request.user.save()

        success = True

    return render(request, 'profile.html', {
        'client' : client,
        'success': success,
        'company': company,
    })

def about(request):
    company = CompanyProfile.objects.first()
    return render(request, 'about.html', {'company': company})


def contact(request):
    company = CompanyProfile.objects.first()
    success = False

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        ContactMessage.objects.create(
            name    = name,
            email   = email,
            phone   = phone,
            subject = subject,
            message = message,
        )
        success = True

    return render(request, 'contact.html', {
        'company': company,
        'success': success,
    })


def tracking(request):
    quotation  = None
    all_items  = []
    error      = None
    company    = CompanyProfile.objects.first()

    if request.method == 'POST':
        code = request.POST.get('quotation_number', '').strip().upper()
        if code:
            quotation = Quotation.objects.prefetch_related('items__product').filter(tracking_code=code).first()
            if quotation:
                all_items = quotation.items.all()
            else:
                error = 'No quotation found with that code. Please check and try again.'
        else:
            error = 'Please enter your tracking code.'

    return render(request, 'tracking.html', {
        'quotation': quotation,
        'all_items': all_items,
        'error'    : error,
        'company'  : company,
    })
