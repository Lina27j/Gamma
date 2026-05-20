from django.contrib import admin
from django.urls import path, include
from product.views import product_detail, quotation, products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('quotation/', quotation, name='quotation'),
    path('products/', products, name='products'),
]