from django.contrib import admin
from django.urls import path, include
from product.views import home, product_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('', home, name='home'),
    path('products/', product_list, name='products'),
]

