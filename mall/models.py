import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import F

from accounts.models import User
from system.models import ImageFile
from utils import constants


class Classify(models.Model):
    """  商品分类 """
    uid = models.UUIDField('分类ID', default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    img = models.ImageField('标签主图', max_length=128, upload_to='classify/', null=True, blank=True)
    name = models.CharField('名称', max_length=128)
    code = models.CharField('编码', max_length=32, null=True, blank=True)
    desc = models.CharField('描述', max_length=256, null=True, blank=True)
    is_valid = models.BooleanField('是否有效', default=True)

    order = models.SmallIntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = '商品类别'
        db_table = 'mall_classify'
        ordering = ['-order']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ 标签 """
    name = models.CharField('标签名称', max_length=32)
    code = models.CharField('标签编码', max_length=32, null=True, blank=True)
    img = models.ImageField('标签主图', max_length=128, upload_to='tag/', null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)

    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        db_table = 'mall_tag'
        ordering = ['-reorder']

    def __str__(self):
        return self.name


class Product(models.Model):
    """ 商品信息 """
    uid = models.UUIDField('商品ID', default=uuid.uuid4, editable=False)
    name = models.CharField('名称', max_length=128)
    desc = models.CharField('描述', max_length=256, null=True, blank=True)
    content = RichTextField('商品描述')

    types = models.SmallIntegerField('商品类型', default=constants.PRODUCT_TYPE_ACTUAL, choices=constants.PRODUCT_TYPES)
    price = models.IntegerField('销售价（积分）', default=5)
    origin_price = models.FloatField('原价', default=0)
    img = models.ImageField('商品主图', max_length=128, upload_to='%Y%m/product/', null=True, blank=True)
    imei = models.CharField('商品编号', max_length=64, null=True, blank=True)
    channel = models.CharField('渠道', max_length=32, null=True, blank=True)
    buy_link = models.CharField('购买链接', max_length=256, null=True, blank=True)

    online_time = models.DateTimeField('定时上线时间', null=True, blank=True)
    offline_time = models.DateTimeField('定时下线时间', null=True, blank=True)
    is_valid = models.BooleanField('是否有效', default=True)

    reorder = models.SmallIntegerField('排序', default=0)
    status = models.SmallIntegerField('状态', default=constants.PRODUCT_STATU_LOST,
                                      choices=constants.PRODUCT_STATUS)
    sku_count = models.IntegerField('库存', default=0)
    remain_count = models.IntegerField('剩余', default=0)
    view_count = models.IntegerField('浏览次数', default=0)
    score = models.FloatField('商品评分', default=10.0)

    classes = models.ManyToManyField(Classify, verbose_name='分类',
                                     related_name='classes',
                                     null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签',
                                  related_name='tags',
                                  null=True, blank=True)
    banners = GenericRelation(ImageFile, verbose_name='banner图',
                              related_query_name="banners")

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'
        db_table = 'mall_product'
        ordering = ['-reorder']

    def update_store_count(self, count):
        """ 更新库存 """
        self.remain_count = F('remain_count') - abs(count)
        self.save()
        self.refresh_from_db()

    def get_comment_list(self):
        """  评论列表 """
        return self.comments.filter(is_valid=True)

    def comment_count(self):
        """ 评价总数 """
        return self.get_comment_list().count()

    def __str__(self):
        return self.name


class Comment(models.Model):
    """ 商品评价 """
    product = models.ForeignKey(Product, related_name='comments', verbose_name='商品')
    user = models.ForeignKey(User, related_name='comments', verbose_name='用户')
    desc = models.CharField('评价内容', max_length=256)
    reorder = models.SmallIntegerField('排序', default=0)
    is_anonymous = models.BooleanField('是否匿名', default=True)

    score = models.FloatField('商品评分', default=10.0)
    score_deliver = models.FloatField('配送服务分', default=10.0)
    score_package = models.FloatField('快递包装分', default=10.0)
    score_speed = models.FloatField('送货速度分', default=10.0)

    is_valid = models.BooleanField('是否有效', default=True)
    img_list = GenericRelation(ImageFile,
                               verbose_name='评价晒图',
                               related_query_name="img_list")

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '商品评价'
        verbose_name_plural = '商品评价'
        db_table = 'mall_product_comment'
        ordering = ['-reorder']

    def __str__(self):
        return self.desc
