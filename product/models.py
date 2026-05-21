from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name                = models.CharField(max_length=200, null=False, verbose_name='Product Name')
    dimensions          = models.TextField(null=False, default='')
    colour              = models.TextField(null=False, default='')
    features            = models.TextField(null=False, default='')
    certificate         = models.TextField(null=False, default='')
    optional            = models.TextField(blank=True, default='')
    
    
   
    def __str__(self):
        return self.name
    
    
class ProductVariant(models.Model):   

    
    HEIGHT_U_VALUES = [6, 9, 12, 15, 18, 21, 24, 26, 32, 36, 42, 45, 47]
    HEIGHT_U_CHOICES = [(i, f'{i}U') for i in HEIGHT_U_VALUES]

    DIMENSION_VALUES = [100, 250, 300, 450, 510, 600, 700, 800, 1000, 1200]
    DIMENSION_CHOICES = [(i, f'{i}mm') for i in DIMENSION_VALUES]

    HEIGHT_MM_VALUES = [365, 495, 630, 760, 895, 985, 1100, 1200, 1500, 1720, 2020, 2160, 2250]
    HEIGHT_MM_CHOICES = [(i, f'{i}mm') for i in HEIGHT_MM_VALUES]

    DEPTH_RAIL_VALUES = [350, 500, 600, 650, 700, 800, 850, 900, 1000, 1050, 1100]
    DEPTH_RAIL_CHOICES = [(i, f'{i}mm') for i in DEPTH_RAIL_VALUES]

    STATIC_LOAD_VALUES = [40, 400, 500, 600, 800, 1100]
    STATIC_LOAD_CHOICES = [(i, f'{i}kg') for i in STATIC_LOAD_VALUES]

    COLOR_CHOICES = [
        ('RAL 9005', 'BLACK (RAL 9005)'),
        ('RAL7035', 'Light Gray (RAL 7035)'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    height_U = models.PositiveSmallIntegerField(null=True,choices=HEIGHT_U_CHOICES)
    width_mm = models.PositiveIntegerField(choices=DIMENSION_CHOICES)
    depth_mm = models.PositiveIntegerField(choices=DIMENSION_CHOICES)
    height_mm = models.PositiveSmallIntegerField(choices=HEIGHT_MM_CHOICES)
    depth_rail_mm = models.PositiveIntegerField(null=True, choices=DEPTH_RAIL_CHOICES)
    static_load_kg = models.PositiveIntegerField(null=True, choices=STATIC_LOAD_CHOICES)
    description = models.TextField(null=False, default='')

    color     = models.CharField(max_length=20, choices=COLOR_CHOICES, default='RAL7035')
    sku       = models.CharField(max_length=100, unique=True, blank=True)  # e.g. GAMMA-6U-600-600
    is_active = models.BooleanField(default=True)
    data_sheet = models.FileField(blank= True, null=True, upload_to='pdfs/')  
    uploaded_at = models.DateTimeField(blank= True, null=True, auto_now_add=True)


class Image(models.Model):  
    name   = models.CharField(max_length=100, blank=True) 
    image  = models.ImageField(upload_to='products/', blank=True, null=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='image'
    )

class Quotation(models.Model):

    MATERIAL_CHOICES = [
        ('galvanised', 'Galvanised'),
        ('steel',      'Steel'),
        ('aluminum',   'Aluminum'),
        ('stainless',  'Stainless Steel'),
    ]

    DOOR_CHOICES = [
        ('glass',       'Glass'),
        ('metal',       'Metal'),
        ('perforated',  'Perforated'),
    ]

    name           = models.CharField(max_length=100)
    company        = models.CharField(max_length=100)
    email          = models.EmailField()
    phone          = models.CharField(max_length=20, blank=True)
    product        = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    quantity       = models.PositiveIntegerField(null=True, blank=True)
    number_of_fans = models.PositiveIntegerField(null=True, blank=True)
    material_type  = models.CharField(max_length=20, choices=MATERIAL_CHOICES, blank=True)
    door_type      = models.CharField(max_length=20, choices=DOOR_CHOICES, blank=True)
    accessories    = models.TextField(blank=True)
    reference_file = models.FileField(upload_to='quotations/', blank=True, null=True)
    message        = models.TextField(blank=True)
    submitted_at   = models.DateTimeField(auto_now_add=True)
    user           = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.name} - {self.company}"
