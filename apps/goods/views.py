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
from rest_framework_extensions.cache.mixins import CacheResponseMixin


class GoodsViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
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


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViweSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    轮播图
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class IndexCategoryViewset(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
