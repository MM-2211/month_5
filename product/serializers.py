from rest_framework import serializers
from .models import *

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = 'name products_count'.split()

    def get_products_count(self, obj):
        products_all = obj.products.all()
        return len(products_all)

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = 'title price category_name reviews'.split()

    def get_category_name(self, product):
        return product.category.name if product.category_id else None


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = 'title reviews average_rating'.split()

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum([i.stars for i in reviews]) / reviews.count(), 2)
        return None

