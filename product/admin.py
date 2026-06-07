from django.contrib import admin
from .models import Product, ProductVariant, Image, Quotation, QuotationItem


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3 
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    inlines = [ProductVariantInline, ImageInline]  

class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 0

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display    = ['id', 'name', 'company', 'email', 'phone', 'submitted_at', 'status']
    list_filter     = ['submitted_at', 'status']
    search_fields   = ['name', 'company', 'email']
    readonly_fields = ['submitted_at']
    inlines         = [QuotationItemInline]

@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display  = ['id', 'quotation', 'width', 'height', 'depth', 'quantity', 'material', 'door']
    search_fields = ['quotation__name', 'quotation__company']