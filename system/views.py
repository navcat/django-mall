from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView

from system.models import News
from utils.verify import VerifyCode


class NewsList(ListView):
    """ 新闻列表 """
    paginate_by = 5
    template_name = 'system/news_list.html'
    queryset = News.objects.filter(is_valid=True)


class NewsInfo(DetailView):
    """ 新闻详情 """
    template_name = 'system/news_info.html'
    queryset = News.objects.filter(is_valid=True)

    def get_object(self, queryset=None):
        """ 使新闻的阅读量增加 1 """
        object = super().get_object(queryset)
        object.view_count += 1
        object.save()
        return object


def set_verify_code(request):
    """ 显示验证码"""
    code = VerifyCode(request)
    code.type = 'world'
    return code.display()
