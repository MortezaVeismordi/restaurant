from rest_framework import serializers
from menu.models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'image', 'is_available', 'ingredients', 'preparation_time',
            'calories', 'slug', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

class MenuItemDetailSerializer(MenuItemSerializer):
    category = CategorySerializer(read_only=True) 