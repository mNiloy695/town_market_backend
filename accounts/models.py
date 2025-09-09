from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

TYPE_ROLES=[
    ('customer','customer'),
    ('shop_owner','shop_owner'),
]
class CustomUser(AbstractUser):
    phone=models.CharField(max_length=11,null=True,blank=True,unique=True)
    profile_photo=models.ImageField(upload_to='account/profile',blank=True,null=True)
    user_type=models.CharField(max_length=30,choices=TYPE_ROLES,default='customer')
    
    


