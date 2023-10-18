from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from logistic.serializers import ProductSerializer, StockSerializer
from logistic.models import Product, Stock

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['address', 'products']


@api_view(['GET'])
def sample_view(request):
    return Response({'message': 'Новый текст для страницы!'})