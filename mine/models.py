from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from accounts.models import User
from mall.models import Product
from system.models import ImageFile
from utils import constants


class Order(models.Model):
    """ 订单 """
    sn = models.CharField('订单号', max_length=32)
    user = models.ForeignKey(User, verbose_name='购买用户', related_name='orders')
    buy_count = models.IntegerField('商品总数', default=1)
    buy_amount = models.FloatField('商品总额', default=1)

    to_user = models.CharField('收货人', max_length=32)
    to_area = models.CharField('省市区', max_length=256)
    to_addr = models.CharField('收货地址', max_length=256)
    to_phone = models.CharField('联系电话', max_length=32)
    remark = models.CharField('备注', max_length=128, null=True, blank=True)

    express_type = models.CharField('快递', max_length=32, null=True, blank=True)
    express_no = models.CharField('运单号', max_length=32, null=True, blank=True)

    status = models.SmallIntegerField('交易状态',
                                      default=constants.TRANS_STATU_SUBMIT,
                                      choices=constants.TRANS_STATUS)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '订单列表'
        verbose_name_plural = '订单列表'
        db_table = 'mine_order'
        ordering = ['-created_at']


class Collection(models.Model):
    """ 我的收藏 """
    product = models.ForeignKey(Product, verbose_name='产品')
    user = models.ForeignKey(User, verbose_name='用户')
    remark = models.CharField('备注', max_length=64, null=True, blank=True)

    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '我的收藏'
        verbose_name_plural = '我的收藏'
        db_table = 'mine_collection'
        ordering = ['-created_at']


class Cart(models.Model):
    """ 我的购物车 """
    product = models.ForeignKey(Product, verbose_name='产品')
    order = models.ForeignKey(Order, verbose_name='订单', related_name='carts', null=True, blank=True)

    user = models.ForeignKey(User, verbose_name='用户', related_name='carts')
    count = models.PositiveIntegerField('购买数量', default=1)
    status = models.SmallIntegerField('状态', choices=constants.TRANS_STATUS,
                                      default=constants.TRANS_STATU_INIT)
    # 商品快照
    name = models.CharField('商品名称', max_length=128)
    img = models.ImageField('商品主图', max_length=256, null=True, blank=True)
    price = models.IntegerField('销售价（积分）', default=5)
    origin_price = models.FloatField('原价', default=0)
    amount = models.FloatField('总和', default=0)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '我的购物车'
        verbose_name_plural = '我的购物车'
        db_table = 'mine_cart'
        ordering = ['-created_at']
