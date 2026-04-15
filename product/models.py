from django.db import models

class Product(models.Model):
    name            = models.CharField(max_length=200, null=False, verbose_name='Product Name')
    features        = models.TextField(null=False, default='')
    certificate     = models.TextField(null=False, default='')
    
   
    def __str__(self):
        return self.name
    
    
class ProductVariant(models.Model):   

    HEIGHT_CHOICES = [
        (6, '6U'), (9, '9U'), (12, '12U'),
        (15, '15U'), (18, '18U'), (21, '21U'),
    ]

    DIMENSION_CHOICES = [
        (600, '600mm'),
        (800, '800mm'),
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

    height_u = models.PositiveSmallIntegerField(choices=HEIGHT_CHOICES)
    width_mm = models.PositiveIntegerField(choices=DIMENSION_CHOICES)
    depth_mm = models.PositiveIntegerField(choices=DIMENSION_CHOICES)

    color     = models.CharField(max_length=20, choices=COLOR_CHOICES, default='RAL7035')
    sku       = models.CharField(max_length=100, unique=True, blank=True)  # e.g. GAMMA-6U-600-600
    is_active = models.BooleanField(default=True)

class Image(models.Model):  
    name   = models.CharField(max_length=100, blank=True) 
    image  = models.ImageField(upload_to='products/', blank=True, null=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='image'
    )
