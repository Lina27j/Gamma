from django.contrib import admin
from .models import Product, ProductVariant, Image


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3 
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['features']
    search_fields = ['name']
    inlines = [ProductVariantInline, ImageInline]  

