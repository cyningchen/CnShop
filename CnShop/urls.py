"""CnShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from CnShop.settings import MEDIA_ROOT
from django.views.static import serve
from apps.goods.views import GoodsViewSet, CategoryViewSet, HotSearchsViewset, BannerViweSet, IndexCategoryViewset
from apps.users.views import SmsCodeViewSet, UserViewSet
from apps.trade.views import ShoppingCartViewSet, OrderViewSet
from apps.user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from rest_framework.documentation import include_docs_urls
import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()
# 商品显示
router.register(r'goods', GoodsViewSet, base_name='goods')
# 商品分类
router.register(r'categorys', CategoryViewSet, base_name='categorys')
# 热搜
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")
# 发送验证码
router.register(r'codes', SmsCodeViewSet, base_name="codes")
# 用户注册和显示
router.register(r'users', UserViewSet, base_name='users')
# 用户收藏功能
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
# 用户留言功能
router.register(r'messages', LeavingMessageViewSet, base_name='messages')
# 用户收货地址
router.register(r'address', AddressViewSet, base_name='address')
# 购物车
router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')
# 订单相关
router.register(r'orders', OrderViewSet, base_name='orders')
# 轮播图
router.register(r'banners', BannerViweSet, base_name='banners')
# 首页商品系列数据
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'docs/', include_docs_urls(title='生鲜')),
    url(r'^login/', obtain_jwt_token),
]
