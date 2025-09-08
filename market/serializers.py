from rest_framework  import serializers
from .models import MarketModel,ShopModel,ItemModel,PurchaseModel


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model=MarketModel
        fields='__all__'
        read_only_fields=['id','created_at','updated_at']

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShopModel
        fields='__all__'
        read_only_fields=['id','created_at','updated_at']


#item serializer

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ['id', 'name', 'description', 'price', 'stock', 'logo', 'active', 'slug', 'shop', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'slug']



class PurchaseModelSerialzier(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model=PurchaseModel
        fields='__all__'
        read_only_fields = ['created_at', 'updated_at', 'total_price', 'item_name', 'item_price']
    
    def validate_quantity(self,value):
        if value<=0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    

