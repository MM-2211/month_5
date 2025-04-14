from django.contrib import admin
from product.models import Category, Product, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
