from django.shortcuts import render
from .serializers import GoodsSerializer

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Goods
from rest_framework import mixins, generics, viewsets
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import GoodsFilter


class GoodsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    商品列表页,分页,搜索,过滤,排序
    """

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()
    #     serializer = GoodsSerializer(goods, many=True)
    #     return Response(serializer.data)
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    分类列表页
    """

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()
    #     serializer = GoodsSerializer(goods, many=True)
    #     return Response(serializer.data)
    queryset = GoodsCategory.objects.all().order_by('id')
    serializer_class = CategorySerializer
    # pagination_class = MyPagination
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    # search_fields = ('name', 'goods_brief', 'goods_desc')
    # ordering_fields = ('sold_num', 'shop_price')