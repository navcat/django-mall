from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from mine import views

urlpatterns = [
    # 我的订单列表
    url(r'^order/list/$', login_required(views.OrderList.as_view()), name='order_list'),
    # 订单详情
    url(r'^order/info/(?P<sn>\S+)/$', login_required(views.OrderDetail.as_view()), name='order_info'),
    # 我的收藏
    url(r'^product/collect/list/$', login_required(views.CollectList.as_view()), name='product_collect_list'),
    # 添加收藏
    url(r'^product/collect/add/(?P<pk>\S+)/$', views.collect_add, name='product_collect_add'),
    # 添加到我的购物车
    url(r'^product/cart/add/(?P<pk>\S+)/$', views.cart_add, name='cart_add'),
    # 提交订单
    url(r'^order/submit/$', views.order_submit, name='order_submit'),
    # 订单支付
    url(r'^order/pay/(?P<sn>\S+)/$', views.order_pay, name='order_pay'),
]