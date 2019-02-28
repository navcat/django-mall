from django.contrib import admin

from system.models import Slider, News, ImageFile


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    """ 轮播图 """
    list_per_page = 20
    list_display = ('desc', 'img', 'types', 'target_url', 'order',
                    'is_valid', 'created_at')
    search_fields = ('desc',)


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    """ 图片管理 """
    list_per_page = 20
    list_display = ('summary', 'img', 'content_type', 'content_object',
                    'is_valid', 'created_at')
    search_fields = ('summary', )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """ 新闻管理 """
    list_per_page = 20
    list_display = ('title', 'types', 'source', 'is_top', 'order', 'view_count',
                    'start_time', 'end_time', 'is_valid', 'created_at')
    search_fields = ('title',)
