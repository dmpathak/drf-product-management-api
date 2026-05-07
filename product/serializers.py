from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from product.models import Category, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['is_deleted']


class ProductSerializer(ModelSerializer):
    category_id = serializers.ReadOnlyField(source='category.id')
    category_name = serializers.ReadOnlyField(source='category.category_name')

    class Meta:
        model = Product
        fields = ['id', 'category_id', 'category_name', 'product_name', 'product_description', 'product_price', 'currency', 'stock_quantity', 'sku', 'image_url']
