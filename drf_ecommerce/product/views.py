from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Brand, Product
from drf_spectacular.utils import extend_schema

from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
)


class CategoryViewSet(viewsets.ViewSet):

    queryset = Category.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):

    category = CategorySerializer()
    brand = BrandSerializer()
    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
    )
    def list_product_by_category(self, request, category=None):
        """
        List all products by category
        """
        serializer = ProductSerializer(
            self.queryset.filter(category__name=category), many=True)
        return Response(serializer.data)
