from django.conf.urls import url

from accounts import views

urlpatterns = [
    # 登录、退出
    url(r'^user/login/$', views.sign_in, name='sign_in'),
    url(r'^user/logout/$', views.sign_out, name='sign_out'),
    # 注册
    url(r'^user/regist/$', views.sign_up, name='sign_up'),
    # 修改密码
    url(r'^user/change/pwd/$', views.change_pwd, name='change_password'),
    # 地址列表
    url(r'^addr/list/$', views.address_list, name='address_list'),
    # 地址编辑
    url(r'^addr/edit/(?P<pk>\S+)/$', views.address_edit, name='address_edit'),
    # 删除地址
    url(r'^addr/delete/(?P<pk>\d+)/$', views.address_delete, name='address_delete'),
]