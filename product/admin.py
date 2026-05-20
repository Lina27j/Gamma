from django.contrib import admin
from .models import Product, ProductVariant, Image, Quotation


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

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display  = ['id','name', 'company', 'email', 'phone', 'product', 'quantity', 'submitted_at']
    list_filter   = ['submitted_at', 'material_type', 'door_type']
    search_fields = ['name', 'company', 'email']
    readonly_fields = ['submitted_at']
    fieldsets = [
        ('Client Info', {
            'fields': ['name', 'company', 'email', 'phone']
        }),
        ('Product Details', {
            'fields': ['product', 'quantity', 'number_of_fans', 'material_type', 'door_type', 'accessories']
        }),
        ('Additional', {
            'fields': ['reference_file', 'message', 'submitted_at']
        }),
    ]