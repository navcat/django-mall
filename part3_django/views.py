from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from system.models import News, Slider
from mall.models import Product
from utils import constants


def index(request):
    """ 首页 """
    # 新闻列表
    news_list = News.objects.filter(is_valid=True, is_top=True)
    # 轮播图列表
    slider_list = Slider.objects.filter(is_valid=True,
                                        types=constants.SLIDER_TYPE_INDEX).order_by('-order')
    # 精选商品推荐列表
    jxtj_list = Product.objects.filter(is_valid=True, tags__code='jxtj')
    # 酒水推荐列表
    jstj_list = Product.objects.filter(is_valid=True, tags__code='jstj')
    # 猜你喜欢
    cnxh_list = Product.objects.filter(is_valid=True, tags__code='cnxh')
    return render(request, 'index.html', {
        'news_list': news_list,
        'slider_list': slider_list,
        'jxtj_list': jxtj_list,
        'jstj_list': jstj_list,
        'cnxh_list': cnxh_list,
    })


def classify(request):
    """ 分类页 """
    return render(request, 'classify.html')


def cart(request):
    """ 购物车 """
    return render(request, 'shopcart.html', {})


@login_required
def mine(request):
    """ 个人中心 """
    return render(request, 'mine.html')
