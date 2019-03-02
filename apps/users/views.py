from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins, viewsets
from apps.users.serializers import UserRegSerializer, SmsSerializer, UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.utils.yunpian import YuanPian
from CnShop.settings import APIKEY
from random import choice
from .models import VerifyCode
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yunpian = YuanPian(APIKEY)
        code = self.generate_code()
        sms_status = yunpian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    authentication_classes = [JSONWebTokenAuthentication, authentication.SessionAuthentication]

    def create(self, request, *args, **kwargs):
        """
        重载create方法，设置name和token，实现注册后立即登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated(), ]
        elif self.action == "create":
            return []
        return []

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer
