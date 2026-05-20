from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from .models import Product,ProductVariant,Image, Quotation
from .serializers import ProductSerializer,ProductVariantSerializer, ImageSerializer
import json
from django.core.paginator import Paginator

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('variants', 'image').all()
    serializer_class = ProductSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def home(request):
    images = list(range(1, 32))  
    pages = [images[i:i+9] for i in range(0, len(images), 9)]
    return render(request, 'home.html', {
        'pages': pages
    })

def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related('variants', 'image'), pk=pk
    )
    related_products = Product.objects.prefetch_related('image').exclude(pk=pk)[:3]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
    })



def quotation(request):
    products = Product.objects.prefetch_related('variants').all()

    products_data = {}
    for p in products:
        variants = list(p.variants.values(
            'height_U', 'width_mm', 'height_mm', 'depth_mm', 'color'
        ))
        products_data[str(p.id)] = {'name': p.name, 'variants': variants}

    success = False

    if request.method == 'POST':
        accessories = ', '.join(request.POST.getlist('accessories'))

        config = []
        if request.POST.get('width_mm'):
            config.append(f"Width: {request.POST['width_mm']}mm")
        if request.POST.get('height_mm'):
            config.append(f"Height: {request.POST['height_mm']}mm")
        if request.POST.get('depth_mm'):
            config.append(f"Depth: {request.POST['depth_mm']}mm")
        if request.POST.get('color'):
            config.append(f"Colour: {request.POST['color']}")

        message = '\n'.join(config)
        if request.POST.get('message'):
            message += '\n\nNote: ' + request.POST['message']

        product = None
        try:
            pid = request.POST.get('product')
            if pid:
                product = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            pass

        Quotation.objects.create(
            name           = request.POST.get('name', ''),
            company        = request.POST.get('company', ''),
            email          = request.POST.get('email', ''),
            phone          = request.POST.get('phone', ''),
            product        = product,
            quantity       = request.POST.get('quantity') or None,
            number_of_fans = request.POST.get('number_of_fans') or None,
            material_type  = request.POST.get('material_type', ''),
            door_type      = request.POST.get('door_type', ''),
            accessories    = accessories,
            reference_file = request.FILES.get('reference_file'),
            message        = message,
        )
        success = True

    return render(request, 'quotation.html', {
        'products'        : products,
        'products_json'   : json.dumps(products_data),
        'success'         : success,
        'initial_product' : request.GET.get('product', ''),
        'material_choices': Quotation.MATERIAL_CHOICES,
        'door_choices'    : Quotation.DOOR_CHOICES,
    })
    



def products(request):
    

    search   = request.GET.get('search', '').strip()
    category = request.GET.get('filter', 'all')

    products = Product.objects.prefetch_related('image').all()

    if search:
        products = products.filter(name__icontains=search)

    if category and category != 'all':
        products = products.filter(name__icontains=category.replace('-', ' '))

    total     = products.count()
    paginator = Paginator(products, 6)
    page      = request.GET.get('page', 1)
    products  = paginator.get_page(page)

    return render(request, 'products.html', {
        'products': products,
        'search'  : search,
        'category': category,
        'total'   : total,
    })