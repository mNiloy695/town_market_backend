from django.shortcuts import render
from .models import MarketModel,ShopModel,ItemModel,PurchaseModel
from .serializers import MarketSerializer,ShopSerializer,ItemSerializer,PurchaseModelSerialzier
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..accounts.email import send_email
class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.shop.owner==request.user


#IsOwner for ItemModel
class IsOwnerPermissionForItemModel(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner==request.user
    

#Custom permission for itemModel 
class CustomPermissionForItemModel(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['POST']:
            return request.user.is_authenticated and hasattr(request.user,'shop')
        return request.user.is_authenticated and request.user.is_staff
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
      
        return obj.shop.owner==request.user
    
# Create your views here.


class MarketModelViewSet(viewsets.ModelViewSet):
    queryset=MarketModel.objects.all()
    serializer_class=MarketSerializer
    filter_backends=[SearchFilter]
    search_fields=['name','district','upazila']
    

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        
        return [permissions.IsAdminUser()]


class ShopModelViewSet(viewsets.ModelViewSet):
    queryset=ShopModel.objects.select_related('market','owner').all()
    serializer_class=ShopSerializer
    filter_backends=[SearchFilter,DjangoFilterBackend]
    search_fields=['name','market__name']
    filterset_fields=['market','owner']
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        
        
        elif self.request.method in ['POST','DELETE'] :
            return [permissions.IsAdminUser()]
        
        elif self.request.method in ['PUT','PATCH']:
            return [permissions.IsAdminUser(),IsOwnerPermission()]
        else:
            return [permissions.IsAdminUser()]
        

# itmes viewset
    
class ItemModelViewSet(viewsets.ModelViewSet):
    queryset=ItemModel.objects.all().select_related('shop','shop__market')
    serializer_class=ItemSerializer
    filter_backends=[SearchFilter,DjangoFilterBackend]
    search_fields=['name','shop__name','shop__market__name','slug']
    filterset_fields=['shop','active']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        
        elif self.request.method in ['POST','PUT','PATCH','DELETE']:
            return [CustomPermissionForItemModel()]
        
        return [permissions.IsAdminUser()]

#custom permission for the user

class CustomPermissionForPurchase(permissions.BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if obj.orderer==request.user:
            if obj.status=="pending" and request.method in ["PATCH"]:
                    return request.data.get("status","").lower()=="cancel"
                
            if request.method in permissions.SAFE_METHODS:
                return True
            
        #shop woner can update the all purchase model
        if getattr(request.user,'user_type',None)  == "shop_owner":
            if obj.item.shop.owner==request.user:
                if request.data.get("status",None):
                    return True
                else:
                    return False
            return False

        return False

class PurchaseModelViewSet(viewsets.ModelViewSet):
    queryset=PurchaseModel.objects.all().select_related('item','orderer','item__shop')
    serializer_class=PurchaseModelSerialzier
    permission_classes = [CustomPermissionForPurchase]

    def get_queryset(self):
        
        user=self.request.user 

        if user.is_staff:
            return  PurchaseModel.objects.all()
        if getattr(user,"user_type",None) =="shop_owner":
            return PurchaseModel.objects.filter(item__shop__owner=user)
        
        return PurchaseModel.objects.filter(orderer=user)
