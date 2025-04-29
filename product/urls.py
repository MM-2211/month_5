from django.urls import path
from product import views

urlpatterns = [
    path("product", views.product_list_api_view),
    path("product/<int:id>/", views.product_detail_api_view),
    path("reviews/", views.review_product_list_api_view),
    path("categories/", views.category_list_api_view),
    path("categories/<int:id>/", views.category_detail_api_views),
    path("api/v1/reviews/", views.review_list_api_view),
    path("reviews/<int:id>/", views.review_detail_api_view),
]