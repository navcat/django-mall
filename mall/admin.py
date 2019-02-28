from django.contrib import admin

from mall.models import Product, Classify, Comment, Tag


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ 商品信息 """
    list_display = ['name', 'types', 'price', 'status', 'img', 'is_valid',
                    'reorder', 'created_at', 'online_time', 'offline_time']
    list_filter = ('types', 'status', )
    search_fields = ('name', )


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    """ 商品分类 """
    list_display = ['uid', 'name', 'code', 'parent', 'created_at']
    search_fields = ('name', 'code',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ 商品标签 """
    list_display = ['name', 'code', 'is_valid', 'created_at']
    search_fields = ('name', 'code',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ 商品评论 """
    list_display = ['product', 'user', 'desc', 'reorder', 'is_anonymous',
                    'score', 'score_deliver', 'score_package', 'score_speed']
    search_fields = ('product__name', 'user__username',)
