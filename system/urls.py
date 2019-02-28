from django.conf.urls import url

from system import views

urlpatterns = [
    # 新闻列表
    url(r'^news/list/$', views.NewsList.as_view(), name='news_list'),
    # 新闻详情
    url(r'^news/info/(?P<pk>\d+)/$', views.NewsInfo.as_view(), name='news_info'),
    # 设置验证码
    url(r'^verify/code/$', views.set_verify_code, name='set_verify_code'),
]