from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import (ProductSerializer,
                          ProductDetailSerializer,
                          CategorySerializer,
                          ReviewSerializer,
                          ProductReviewSerializer,
                          ProductValidateSerializer,
                          CategoryValidateSerializer,
                          ReviewValidateSerializer)




@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_views(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'Category does not exist'})
    if request.method == 'GET':
        data = CategorySerializer(category).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,)
    else:
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data,
                        status=status.HTTP_200_OK)
    else:
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = serializer.validated_data.get('name')

        category = Category.objects.create(
            name=name
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)




@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Product not found'})
    if request.method == 'GET':
        data = ProductDetailSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    else:
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.select_related("category").all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data,
                        status=status.HTTP_200_OK)

    else:
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data('category_id')


        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)




@api_view(http_method_names=['GET'])
def review_product_list_api_view(request):
    products = Product.objects.prefetch_related("reviews").all()
    data = ProductReviewSerializer(products, many=True).data
    return Response(data=data,
                    status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Review does not exist'})
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)
    else:
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data,
                        status=status.HTTP_200_OK)
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')

        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)
