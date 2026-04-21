from rest_framework import serializers
from .models import Product,ProductVariant,Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Image
        fields = ['id', 'name', 'image']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductVariant
        fields = ['id', 'height_u', 'width_mm', 'depth_mm', 'color', 'sku', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    variants   = ProductVariantSerializer(many=True, read_only=True)
    image      = ImageSerializer(many=True, read_only=True)
    class Meta:
        model  = Product
        fields = '__all__'
