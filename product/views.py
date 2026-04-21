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