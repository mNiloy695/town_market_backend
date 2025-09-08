from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import MarketModelViewSet,ShopModelViewSet,ItemModelViewSet,PurchaseModelViewSet
router=DefaultRouter()
router.register('market/list',MarketModelViewSet)
router.register('shops/list',ShopModelViewSet)
router.register('items/list',ItemModelViewSet)
router.register('item/purchase',PurchaseModelViewSet)

urlpatterns = [
    path('',include(router.urls)),
    
]
