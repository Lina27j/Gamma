from django.urls import path
from . import views
from product.views import product_detail, quotation, products


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('quotation/', quotation, name='quotation'),
    path('products/', products, name='products'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
]