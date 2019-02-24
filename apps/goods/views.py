from django.shortcuts import render
from .serializers import GoodsSerializer

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Goods
from rest_framework import mixins, generics
from .models import *
from .serializers import *


class GoodsListView(generics.ListAPIView):
    """
    List all snippets, or create a new snippet.
    """

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()
    #     serializer = GoodsSerializer(goods, many=True)
    #     return Response(serializer.data)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = MyPagination
