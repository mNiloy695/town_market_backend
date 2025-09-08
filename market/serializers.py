from rest_framework  import serializers
from .models import MarketModel,ShopModel,ItemModel


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

    