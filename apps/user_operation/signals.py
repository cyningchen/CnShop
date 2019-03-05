# -*- coding:utf-8 -*-
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserFav


@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    """
    信号量, 一旦捕捉到User为create就触发
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
