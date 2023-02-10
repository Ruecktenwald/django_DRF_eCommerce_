from rest_framework import serializers
from .models import Product, Category, Brand, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category_name', ]


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        exclude = ('id',)


class ProductLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLine
        exclude = ('id', 'product', 'is_active')


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    category_name = serializers.CharField(source='category.name')
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description',
                  'brand_name', 'category_name', 'category', 'product_line',)
