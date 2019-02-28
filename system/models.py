from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from ckeditor.fields import RichTextField

from utils import constants


class Slider(models.Model):
    """ 轮播图配置 """
    types = models.SmallIntegerField('类型',
                                     choices=constants.SLIDER_TYPES_CHOICES,
                                     default=constants.SLIDER_TYPE_INDEX)
    desc = models.CharField('描述1', max_length=255, null=True, blank=True)
    tips = models.CharField('描述2', max_length=255, null=True, blank=True)
    order = models.SmallIntegerField('排序', help_text='数字越大越靠前', default=0)
    img = models.ImageField('图片地址',  upload_to='silder')
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    target_url = models.URLField('点击后的跳转地址', null=True, blank=True)

    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        db_table = 'system_slider'
        verbose_name = '轮播图配置'
        verbose_name_plural = '轮播图配置'
        ordering = ['-order']

    def __str__(self):
        return self.desc or ''


class ImageFile(models.Model):
    """ 附件 """
    IMG_TYPE_CHOICES = (
        (0, '图片文件'),
        # 以下类型暂未使用
        # (1, '未知类型'),
        # (2, 'Word文档'),
        # (3, 'PPT文档'),
        # (4, 'Excel文档'),
        # (5, 'PDF'),
        # (6, 'TXT'),
    )
    summary = models.CharField('照片说明', max_length=200)
    img = models.FileField(upload_to='%Y%m/file/', max_length=300)
    thumb_img = models.ImageField(upload_to='%Y%m/file_thumb/', blank=True, null=True, max_length=300)
    types = models.IntegerField('照片类型', choices=IMG_TYPE_CHOICES, default=0)
    space = models.FloatField('附件大小（KB)', default=0)
    width = models.FloatField('原图宽度', default=0)
    height = models.FloatField('原图高度', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = '附件'
        db_table = 'system_img_file'

    def get_img_url(self):
        """ 图片url"""
        if self.img:
            return self.img.url
        return self.img.name

    def get_thumb_img_url(self):
        """ 图片缩略图"""
        if self.thumb_img:
            return self.thumb_img.url
        return self.thumb_img.name


class News(models.Model):
    """ 新闻及通知 """
    TYPES_CHOICES = (
        (1, '新闻'),
        (2, '通知'),
    )
    title = models.CharField('标题', max_length=255, null=True, blank=True)
    content = RichTextField('发送内容', null=True, blank=True)
    source = models.CharField('来源', max_length=30, blank=True, null=True,
                              choices=constants.SOURCE_CHOICES)
    types = models.SmallIntegerField('类型', default=3, choices=TYPES_CHOICES)
    start_time = models.DateTimeField('生效时间', null=True, blank=True)
    end_time = models.DateTimeField('失效时间', null=True, blank=True)
    view_count = models.IntegerField('阅读次数', default=0)
    order = models.SmallIntegerField('排序', help_text='数字越大越靠前', default=0)
    is_top = models.BooleanField('是否置顶', default=False, help_text='置顶后将在首页显示')

    created_at = models.DateTimeField('发送时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)
    is_valid = models.BooleanField('是否有效', default=True)

    class Meta:
        db_table = 'system_news'
        verbose_name = '新闻及通知'
        verbose_name_plural = '新闻及通知'
        ordering = ['-order']

    def __str__(self):
        return self.title
