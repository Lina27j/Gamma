from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductVariant, Image, Quotation, QuotationItem
from Client.models import Client
from .serializers import ProductSerializer, ProductVariantSerializer, ImageSerializer
from company.models import CompanyProfile
import json
import random
import string
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def generate_tracking_code():
    characters = string.ascii_uppercase + string.digits
    code = ''
    for i in range(8):
        code = code + random.choice(characters)
    return code


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
    all_images = list(range(1, 32))

    # split the images into groups of 9
    pages = []
    group = []
    for image in all_images:
        group.append(image)
        if len(group) == 9:
            pages.append(group)
            group = []
    if len(group) > 0:
        pages.append(group)

    return render(request, 'home.html', {'pages': pages})


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related('variants', 'image'), pk=pk
    )
    related_products = Product.objects.prefetch_related('image').exclude(pk=pk)[:3]
    company          = CompanyProfile.objects.first()
    return render(request, 'product_detail.html', {
        'product'         : product,
        'related_products': related_products,
        'company'         : company,
    })

@login_required(login_url='/login/')
def quotation(request):

    error = None

    if request.method == 'POST':

        name    = request.POST.get('name', '').strip()
        company = request.POST.get('company', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()

        if not name:
            error = 'Please enter your full name.'
        elif not company:
            error = 'Please enter your company name.'
        elif not email or '@' not in email:
            error = 'Please enter a valid email address.'
        elif phone:
            
            has_letter = False
            for character in phone:
                if character.isalpha():
                    has_letter = True
                    break
            if has_letter:
                error = 'Phone number must not contain letters.'

        if error is None:
            if request.user.is_authenticated:
                current_user = request.user
            else:
                current_user = None

            my_quotation = Quotation.objects.create(
                user          = current_user,
                name          = name,
                company       = company,
                email         = email,
                phone         = phone,
                tracking_code = generate_tracking_code(),
            )

            return redirect('add_product', my_id=my_quotation.pk)

   
    client  = None
    if request.user.is_authenticated:
        client = Client.objects.filter(user=request.user).first()

    company = CompanyProfile.objects.first()
    return render(request, 'quotation.html', {
        'client' : client,
        'error'  : error,
        'company': company,
    })


def add_product(request, my_id):

    my_quotation = get_object_or_404(Quotation, pk=my_id)

   
    all_products = Product.objects.all()

    
    selected_product_id      = request.GET.get('product_id')
    selected_product = None
    width_list     = []
    height_list    = []
    depth_list     = []
    color_list     = []

   
    if selected_product_id:
        selected_product = Product.objects.prefetch_related('variants').filter(pk=selected_product_id).first()

        if selected_product:
            variant_list = selected_product.variants.all()

            for v in variant_list:
                if v.width_mm not in width_list:
                    width_list.append(v.width_mm)
                if v.height_U is not None and v.height_U not in height_list:
                    height_list.append(v.height_U)
                if v.depth_mm not in depth_list:
                    depth_list.append(v.depth_mm)
                if v.color not in color_list:
                    color_list.append(v.color)

            width_list.sort()
            height_list.sort()
            depth_list.sort()

    error = None

    if request.method == 'POST':

        product_id = request.POST.get('product') or None
        width      = request.POST.get('width', '').strip()
        height     = request.POST.get('height', '').strip()
        depth      = request.POST.get('depth', '').strip()
        color      = request.POST.get('color', '').strip()
        quantity   = request.POST.get('quantity', '').strip()
        material   = request.POST.get('material', '').strip()
        door       = request.POST.get('door', '').strip()

        if not product_id:
            error = 'Please select a cabinet type.'
        elif not width:
            error = 'Please enter the width.'
        elif not height:
            error = 'Please enter the height.'
        elif not depth:
            error = 'Please enter the depth.'
        elif not color:
            error = 'Please enter the colour.'
        elif not quantity or not quantity.isdigit() or int(quantity) < 1:
            error = 'Please enter a valid quantity (number greater than 0).'
        elif not material:
            error = 'Please select a type of material.'
        elif not door:
            error = 'Please select a type of door.'

        if error is None:

            checked_accessories = request.POST.getlist('accessories')
            accessories_text    = ''
            for acc in checked_accessories:
                if accessories_text == '':
                    accessories_text = acc
                else:
                    accessories_text = accessories_text + ', ' + acc

            found_sku = ''
            if product_id:
                variant_list = ProductVariant.objects.filter(product_id=product_id)
                for v in variant_list:
                    if str(v.width_mm) == width and str(v.height_U) == height and str(v.depth_mm) == depth and v.color == color:
                        found_sku = v.sku
                        break

            QuotationItem.objects.create(
                quotation   = my_quotation,
                product_id  = product_id,
                width       = width,
                height      = height,
                depth       = depth,
                color       = color,
                quantity    = int(quantity),
                material    = material,
                door        = door,
                accessories = accessories_text,
                note        = request.POST.get('note', ''),
                sku         = found_sku,
            )

            if request.FILES.get('reference_file'):
                my_quotation.reference_file = request.FILES.get('reference_file')
                my_quotation.save()

            return redirect('add_product', my_id=my_quotation.pk)

    added_items = my_quotation.items.all()
    company     = CompanyProfile.objects.first()

    return render(request, 'add_product.html', {
        'my_quotation'    : my_quotation,
        'all_products'    : all_products,
        'selected_product': selected_product,
        'width_list'      : width_list,
        'height_list'     : height_list,
        'depth_list'      : depth_list,
        'color_list'      : color_list,
        'added_items'     : added_items,
        'material_choices': QuotationItem.MATERIAL_CHOICES,
        'door_choices'    : QuotationItem.DOOR_CHOICES,
        'error'           : error,
        'company'         : company,
    })


def remove_item(request, item_id):

    
    item    = get_object_or_404(QuotationItem, pk=item_id)
    back_id = item.quotation.pk

    item.delete()

    return redirect('add_product', my_id=back_id)


def quotation_print(request, pk):
    my_quotation = get_object_or_404(Quotation, pk=pk)
    all_items    = my_quotation.items.all()
    company      = CompanyProfile.objects.first()

    return render(request, 'quotation_print.html', {
        'quotation': my_quotation,
        'all_items': all_items,
        'company'  : company,
    })


def products(request):

    search   = request.GET.get('search', '').strip()
    category = request.GET.get('filter', 'all')

    product_list = Product.objects.prefetch_related('image').all()

    if search:
        product_list = product_list.filter(name__icontains=search)

    if category != 'all' and category != '':
        category_name = category.replace('-', ' ')
        product_list  = product_list.filter(name__icontains=category_name)

    total     = product_list.count()
    paginator = Paginator(product_list, 6)
    page      = request.GET.get('page', 1)
    products  = paginator.get_page(page)

    company = CompanyProfile.objects.first()
    return render(request, 'products.html', {
        'products': products,
        'search'  : search,
        'category': category,
        'total'   : total,
        'company' : company,
    })
