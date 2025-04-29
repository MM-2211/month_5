from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import *
from .serializers import (ProductSerializer,
                          ProductDetailSerializer,
                          CategorySerializer,
                          ReviewSerializer,
                          ProductReviewSerializer,
                          ProductValidateSerializer,
                          CategoryValidateSerializer,
                          ReviewValidateSerializer)

from django.db.models import Count
from django.shortcuts import get_object_or_404

class CategoryDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Category, id=id)

    def get(self, request, id):
        category = self.get_object(id)
        return Response(data=CategorySerializer(category).data)

    def put(self, request, id):
        category = self.get_object(id)
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data['name']
        category.save()
        return Response(data=CategorySerializer(category).data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.create(name=serializer.validated_data['name'])
        return Response(data=CategorySerializer(category).data, status=status.HTTP_201_CREATED)



class ProductDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Product, id=id)

    def get(self, request, id):
        product = self.get_object(id)
        return Response(data=ProductDetailSerializer(product).data)

    def put(self, request, id):
        product = self.get_object(id)
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data['title']
        product.description = serializer.validated_data['description']
        product.price = serializer.validated_data['price']
        product.category_id = serializer.validated_data['category_id']
        product.save()
        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_200_OK)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.select_related('category').all()
        data = ProductSerializer(products, many=True).data
        return Response(data)

    def post(self, request):
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            price=serializer.validated_data['price'],
            category_id=serializer.validated_data['category_id']
        )
        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)


class ProductReviewListAPIView(APIView):
    def get(self, request):
        products = Product.objects.prefetch_related("reviews").all()
        data = ProductReviewSerializer(products, many=True).data
        return Response(data=data)


class ReviewDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Review, id=id)

    def get(self, request, id):
        review = self.get_object(id)
        return Response(data=ReviewSerializer(review).data)

    def put(self, request, id):
        review = self.get_object(id)
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data['text']
        review.stars = serializer.validated_data['stars']
        review.product_id = serializer.validated_data['product_id']
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        review = self.get_object(id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewListCreateAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(
            text=serializer.validated_data['text'],
            stars=serializer.validated_data['stars'],
            product_id=serializer.validated_data['product_id']
        )
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
