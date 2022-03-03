from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    model = Category
    fields = ['id', 'title', 'parent_category_id', 'created_at', 'updated_at', ]


class ProductSerializer(serializers.ModelSerializer):
    model = Product
    fields = ['id', 'title', 'category', 'price', 'created_at', 'updated_at', ]
