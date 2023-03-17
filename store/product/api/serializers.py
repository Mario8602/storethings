from rest_framework import serializers
from ..models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'price')


class CourseSerializer(serializers.ModelSerializer):
    modules = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug')