from django.views.generic.base import View
from apps.goods.models import Goods
from django.http import HttpResponse,JsonResponse
import json


class GoodsListView(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        json_data1 = json.loads(json_data)
        return JsonResponse(json_data1, safe=False)
