from rest_framework import viewsets
from django.shortcuts import render
from .models import Product,ProductVariant,Image
from .serializers import ProductSerializer,ProductVariantSerializer, ImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('variants', 'image').all()
    serializer_class = ProductSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def home(request):
    images = list(range(1, 32))  
    pages = [images[i:i+9] for i in range(0, len(images), 9)]
    return render(request, 'home.html', {
        'pages': pages
    })