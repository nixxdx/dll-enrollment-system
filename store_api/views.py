from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    DRF Browsable API endpoint displaying all E-commerce products.
    Supports GET (list/detail), POST (create), PUT/PATCH (update), and DELETE.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer