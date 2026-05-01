from django.db import models

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

    HEIGHT_CHOICES = [
    (18, '18U'),
    (21, '21U'),
    (24, '24U'),
    (26, '26U'),
    (32, '32U'),
]

    DIMENSION_CHOICES = [
    (300, '300mm'),
    (400, '400mm'),
    (500, '500mm'),
    (600, '600mm'),
    (700, '700mm'),
    (800, '800mm'),
    (900, '900mm'),
    (1000, '1000mm'),
]

    COLOR_CHOICES = [
        ('RAL7035', 'Light Gray (RAL 7035)'),
        ('custom', 'Custom on Request'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    height_mm = models.PositiveSmallIntegerField(choices=HEIGHT_CHOICES)
    width_mm = models.PositiveIntegerField(choices=DIMENSION_CHOICES)
    depth_mm = models.PositiveIntegerField(choices=DIMENSION_CHOICES)
    depth_rail_mm = models.PositiveIntegerField(null=True, choices=DIMENSION_CHOICES)
    static_load_kg = models.PositiveIntegerField(null=True, choices=DIMENSION_CHOICES)
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
