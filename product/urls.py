from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductVariantViewSet, ImageViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]