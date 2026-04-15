from django.db import models

class Product(models.Model):
    name            = models.CharField(max_length=200, null=False, verbose_name='Product Name')
    features        = models.TextField(null=False, default='')
    certificate     = models.TextField(null=False, default='')
    image_url       = models.URLField(blank=True)
    height          = models.IntegerField()
    depth           = models.IntegerField()
    width           = models.IntegerField()
    color           = models.CharField(max_length=200)

    def __str__(self):
        return self.name

