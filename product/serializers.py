from rest_framework import serializers
from .models import Product,ProductVariant,Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Image
        fields = ['id', 'name', 'image']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductVariant
        fields = ['id','height_U','width_mm','depth_mm', 'height_mm',
            'depth_rail_mm','static_load_kg','description','color',
            'sku','is_active','data_sheet','uploaded_at']

class ProductSerializer(serializers.ModelSerializer):
    variants   = ProductVariantSerializer(many=True, read_only=True)
    image      = ImageSerializer(many=True, read_only=True)
    class Meta:
        model  = Product
        fields = '__all__'
