import re

from django import forms
from django.db import transaction
from django.contrib.auth import authenticate

from accounts.models import UserAddress, User, UserProfile
from utils.forms import VerifyCodeForm


class LoginForm(VerifyCodeForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.user = None

    username = forms.CharField(label='用户名', required=True, error_messages={
        'required': '请输入用户名'
    })
    password = forms.CharField(label='密码', required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', None)
        password = cleaned_data.get('password', None)
        # 验证用户名或密码
        user = authenticate(username=username, password=password)
        self.user = user
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        return cleaned_data


class UserAddressForm(forms.ModelForm):
    """  地址新增与编辑 """
    region = forms.CharField(label='大区域', max_length=32, required=True, error_messages={
        'required': '请选择地址'
    })

    class Meta:
        model = UserAddress
        fields = ('address', 'username', 'phone', 'is_default')
        widgets = {
            'is_default': forms.CheckboxInput(attrs={
                'class': 'weui-switch'
            })
        }
        error_messages = {
            'username': {
                'required': '请输入收件人信息'
            },
            'phone': {
                'required': '请输入收件人手机号码'
            },
            'address': {
                'required': '请输入详细地址'
            }
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_phone(self):
        data = self.cleaned_data['phone']
        pattern = r'^0{0,1}(1)[0-9]{10}$'
        if not re.search(pattern, data):
            raise forms.ValidationError('请输入正确的手机号码')
        return data

    def clean(self):
        cleaned_data = super().clean()
        # 验证每个人最多可以添加20个地址
        if self.request.user.user_addrs.filter(is_valid=True).count() >= 20:
            raise forms.ValidationError('最多只能添加20个地址')
        return cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        region = self.cleaned_data['region']
        (province, city, area) = region.split(' ')
        obj.province = province
        obj.city = city
        obj.area = area
        obj.user = self.request.user
        # 如果当前的地址是默认地址，则要设置其他地址为非默认地址
        if self.cleaned_data['is_default']:
            self.request.user.user_addrs.filter(is_valid=True).update(is_default=False)
        obj.save()


class RegisterForm(VerifyCodeForm):
    """ 用户注册 """
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

    username = forms.CharField(label='用户名', required=True, max_length=64, error_messages={
        'required': '请输入用户名'
    })
    password = forms.CharField(label='密码', required=True, max_length=256, widget=forms.PasswordInput(), error_messages={
        'required': '请输入密码'
    })
    password2 = forms.CharField(label='重复密码', required=True, max_length=256, widget=forms.PasswordInput(), error_messages={
        'required': '请输入密码再次确认'
    })
    nickname = forms.CharField(label='昵称', required=True, max_length=64, error_messages={
        'required': '请输入昵称'
    })

    def clean_username(self):
        """ 验证用户名 """
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('该用户名已存在')
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 8:
            raise forms.ValidationError('密码长度至少要8位')
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password', None)
        password2 = cleaned_data.get('password2', None)
        if password != password2:
            raise forms.ValidationError('两次密码输入不正确')
        return cleaned_data

    @transaction.atomic()
    def save(self, commit=False):
        data = self.cleaned_data
        username = data['username']
        password = data['password']
        nickname = data['nickname']
        obj = User.objects.create_user(username=username,
                                       password=password,
                                       nickname=nickname)
        # 创建用户的详细信息
        UserProfile.objects.create(username=obj.username, user=obj)
        # 帮用户登录
        user = authenticate(username=username, password=password)
        return user
