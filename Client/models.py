from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
   firstName   = models.CharField(max_length=200, null=False, verbose_name='First Name')
   lastName    = models.CharField(max_length=200, null=False, verbose_name='Last Name')
   phoneNum    = models.CharField(max_length=200, null=False, verbose_name='Phone Number')
   email       = models.EmailField(null=False, verbose_name='Email')


   user = models.OneToOneField(User, on_delete=models.CASCADE, default=1) 

   def __str__(self):
      return self.firstName+' '+self.lastName
   

