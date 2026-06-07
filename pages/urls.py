from django.urls import path
from . import views
from product.views import product_detail, quotation, products, quotation_print, add_product, remove_item


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
    path('quotation/print/<int:pk>/', quotation_print, name='quotation_print'),
    path('quotation/<int:my_id>/add-product/', add_product, name='add_product'),
    path('quotation/remove-item/<int:item_id>/', remove_item, name='remove_item'),
    path('tracking/', views.tracking, name='tracking'),
    path('profile/', views.update_profile, name='update_profile'),
    path('contact/', views.contact, name='contact'),
]