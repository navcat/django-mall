"""part3_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from part3_django import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 首页、分类页、购物车、个人中心
    url(r'^$', views.index, name='index'),
    url(r'^classify/$', views.classify, name='classify'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine_index'),
    # 用户账户模块
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    # 系统消息
    url(r'^system/', include('system.urls', namespace='system')),
    # 商品系统
    url(r'^mall/', include('mall.urls', namespace='mall')),
    # 个人中心
    url(r'^mine/', include('mine.urls', namespace='mine')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
