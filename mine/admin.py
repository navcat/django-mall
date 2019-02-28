from django.contrib import admin

from mine.models import Order, Collection


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ 订单 """
    list_display = ['sn', 'user', 'to_user', 'to_addr', 'to_phone',
                    'remark', 'express_type', 'express_no', 'created_at']
    search_fields = ('sn', 'to_phone', 'to_user',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """ 用户的收藏 """
    list_display = ['product', 'user', 'remark', 'is_valid', 'created_at']
    search_fields = ('user__username', )
