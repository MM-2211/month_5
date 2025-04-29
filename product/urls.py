from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.ProductListCreateAPIView.as_view()),
    path("product/<int:id>/", views.ProductDetailAPIView.as_view()),
    path("product/reviews/", views.ProductReviewListAPIView.as_view()),
    path("categories/", views.CategoryListCreateAPIView.as_view()),
    path("categories/<int:id>/", views.CategoryDetailAPIView.as_view()),
    path("reviews/", views.ReviewListCreateAPIView.as_view()),
    path("reviews/<int:id>/", views.ReviewDetailAPIView.as_view())
]