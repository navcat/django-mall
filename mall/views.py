from django.db.models import Q
from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView

from mall.models import Product
from utils import constants


class ProductList(ListView):
    """ 商品列表 """
    paginate_by = 4
    template_name = 'mall/pro_list.html'

    def get_queryset(self):
        query = Q(is_valid=True, status=constants.PRODUCT_STATU_SELL)
        # 按照标签搜索
        tags = self.request.GET.get('tag', None)
        if tags:
            query = query & Q(tags__code=tags)
        # 按名称搜索
        name = self.request.GET.get('name', None)
        if name:
            query = query & Q(name__icontains=name)
        return Product.objects.filter(query)


class ProductInfo(DetailView):
    """  商品详情 """
    template_name = 'mall/pro_info.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    queryset = Product.objects.filter(is_valid=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加用户的默认地址
        addr = None
        if self.request.user.is_authenticated:
            try:
                addr = self.request.user.default_addr
            except IndexError:
                pass
        context['default_addr'] = addr
        return context
