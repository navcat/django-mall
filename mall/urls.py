from django.conf.urls import url

from mall import views

urlpatterns = [
    # 商品列表
    url(r'^product/list/$', views.ProductList.as_view(), name='product_list'),
    url(r'^product/load/list/$', views.ProductList.as_view(
        template_name='mall/prod_list_load.html'), name='product_load_list'),
    # 商品详情
    url(r'^product/info/(?P<uid>\S+)/$', views.ProductInfo.as_view(), name='product_info'),
]