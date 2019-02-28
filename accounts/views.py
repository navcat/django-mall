from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from accounts.forms import LoginForm, UserAddressForm, RegisterForm
from accounts.models import UserAddress


def sign_in(request, form_class=LoginForm):
    """ 用户登录"""
    if request.method == 'POST':
        form = form_class(data=request.POST, request=request)
        # print(form.as_p())
        if form.is_valid():
            login(request, form.user)
            messages.success(request, '登录成功')
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
    else:
        form = form_class(request=request)
    return render(request, 'accounts/login.html', {
        'form': form
    })


def sign_out(request):
    """ 用户退出登录"""
    logout(request)
    # 退出登录后跳转到首页
    messages.success(request, '欢迎下次再来!')
    return redirect(reverse('mall:product_list'))


def sign_up(request, form_class=RegisterForm):
    """ 用户注册"""
    if request.method == 'POST':
        # print(request.POST)
        form = form_class(data=request.POST, request=request)
        # print(form.as_p())
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '恭喜！注册成功')
            return redirect('mine_index')
    else:
        form = form_class(request=request)
    return render(request, 'accounts/regist.html', {
        'form': form
    })


@login_required
def change_pwd(request):
    """ 更改密码 """
    return render_to_response('accounts/change_pwd.html')


@login_required
def address_list(request):
    """ 用户地址列表 """
    addr_list = UserAddress.objects.filter(is_valid=True, user=request.user)
    return render(request, 'accounts/address_list.html', {
        'addr_list': addr_list
    })


@login_required
def address_edit(request, pk, form_class=UserAddressForm):
    """ 用户地址编辑 """
    addr = None
    initial = {}
    # pk不是数字，则表示新增
    if pk.isdigit():
        addr = get_object_or_404(UserAddress, pk=pk, user=request.user, is_valid=True)
        initial['region'] = '{0} {1} {2}'.format(addr.province, addr.city, addr.area)
    if request.method == 'POST':
        form = form_class(request=request, data=request.POST, instance=addr, initial=initial)
        if form.is_valid():
            form.save()
            messages.success(request, '操作成功')
            return redirect('accounts:address_list')
    else:
        form = form_class(request=request, instance=addr, initial=initial)
    return render(request, 'accounts/address_edit.html', {
        'form': form
    })


@login_required
# @csrf_exempt
def address_delete(request, pk):
    """ 删除用户地址"""
    try:
        addr = UserAddress.objects.filter(pk=pk, user=request.user, is_valid=True)[0]
        addr.is_valid = False
        addr.save()
    except IndexError:
        return HttpResponse('no')
    return HttpResponse('ok')