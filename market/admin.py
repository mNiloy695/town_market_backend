from django.contrib import admin
from .models import MarketModel,ShopModel,ItemModel,PurchaseModel
# Register your models here.

admin.site.register(MarketModel)
admin.site.register(ShopModel)
admin.site.register(ItemModel)
admin.site.register(PurchaseModel)
