from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your models here.

#Create maket Model here
UPAZILA_CHOIES=[
    ('Feni sadar','Feni sadar'),
    ('Daganbhuiyan','Daganbhuiyan'),
    ('Parshuram','Parshuram'),
    ('Chhagalnaiya','Chhagalnaiya'),
    ('Sonagazi','Sonagazi'),
    ('Fulgazi','Fulgazi'),
]

ORDER_STATUS=[
    ('pending','pending'),
    ("cancel","cancel"),
    ('processing','processing'),
    ('completed','completed'),
    
]
class MarketModel(models.Model):
    name=models.CharField(max_length=100,unique=True)
    location=models.CharField(max_length=200)
    description=models.TextField()
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    district=models.CharField(max_length=100,default='Feni')
    upazila=models.CharField(max_length=100,choices=UPAZILA_CHOIES,null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering=['created_at']
    

#create shop model here

class ShopModel(models.Model):
    name=models.CharField(max_length=100)
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name='shop')
    description=models.TextField()
    market=models.ForeignKey(MarketModel,on_delete=models.CASCADE,related_name='shops')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    logo=models.ImageField(upload_to='shops/logo',null=True,blank=True)
    active=models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['market', 'name'], name='unique_shop_name_per_market')
        ]
        ordering=[
        'created_at'
        ]

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        if self.owner.user_type != "shop_owner":
             self.owner.user_type = "shop_owner"
             self.owner.save()
        return self

class ItemModel(models.Model):
    name=models.CharField(max_length=100)
    shop=models.ForeignKey(ShopModel,on_delete=models.CASCADE,related_name='items')
    description=models.TextField()
    price=models.DecimalField(max_digits=100,decimal_places=2)
    stock=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    logo=models.ImageField(upload_to='items/logo',null=True,blank=True)
    slug=models.SlugField(max_length=300,unique=True,blank=True,null=True)

    class Meta:
        ordering=['created_at']
    def save(self, *args, **kwargs):
        if not self.slug:
           self.slug = f"{slugify(self.name)}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    

class PurchaseModel(models.Model):
    item=models.ForeignKey(ItemModel,on_delete=models.SET_NULL,blank=True,null=True)
    orderer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status=models.CharField(max_length=100,choices=ORDER_STATUS,default='pending')
    address=models.CharField(max_length=500,blank=True,null=True)
    def save(self,*args,**kwargs):
        if self.item:
              self.total_price=self.item.price*self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return self.item.name
