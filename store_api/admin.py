from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'category', 'price', 'stock', 'is_available')
    list_filter = ('brand', 'is_available')
    search_fields = ('name', 'brand', 'description')