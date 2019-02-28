import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F

from utils import constants


class User(AbstractUser):
    """ 用户基础信息 """
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    nickname = models.CharField('昵称', max_length=30, null=True, blank=True)
    last_login = models.DateTimeField('上次登录时间', blank=True, null=True)
    avatar = models.ImageField('个人头像', upload_to='%Y%m/avatar', blank=True)

    status = models.SmallIntegerField('用户状态',
                                      choices=constants.USER_STATUS_CHOICES,
                                      default=constants.USER_STATUS_ACTIVE)
    integral = models.IntegerField('积分', default=0)
    level = models.IntegerField('用户等级',
                                default=constants.USER_LEVEL_COMMON,
                                choices=constants.USER_LEVEL_CHOICES)

    class Meta:
        verbose_name = '用户基础信息'
        verbose_name_plural = '用户基础信息'
        db_table = 'accounts_user'

    def ope_integral_account(self, types, count):
        """ 操作用户的积分账户 """
        if abs(count) == 0:
            return self.integral
        if types == 1:  # 增加
            self.integral = F('integral') + abs(count)
        elif types == 0:  # 消费
            self.integral = F('integral') - abs(count)
        self.save()
        self.refresh_from_db()
        return self.integral

    @property
    def default_addr(self):
        """ 当前用户的默认地址"""
        try:
            addr = self.user_addrs.filter(is_valid=True, is_default=True)[0]
        except IndexError:
            addr = None
        return addr

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """ 用户详细信息"""

    CHANNEL_CHOICES = (
        ('web', '自主注册'),
        ('android', '安卓'),
        ('iphone', '苹果'),
    )
    GENDER_CHOICES = (
        (1, '男'),
        (2, '女'),
    )
    VIP_TYPE_CHOICES = (
        (1, '普通会员'),
        # (2, '月VIP'),
        # (3, '年VIP'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField('用户名', max_length=40, unique=True, db_index=True)

    is_verified = models.BooleanField('是否已通过验证', default=False)
    real_name = models.CharField('真实姓名', max_length=30, null=True, blank=True)
    invite_code = models.CharField('邀请码', max_length=16, null=True, blank=True)

    # 联系方式
    mobile_no = models.CharField('手机号码', max_length=11, null=True, blank=True)
    is_mobile_no_verified = models.BooleanField('手机号是否已验证', default=False)
    signature = models.CharField('个性签名', max_length=255, null=True, blank=True)

    user_type = models.SmallIntegerField('用户类型',
                                         choices=constants.USER_TYPE_CHOICES,
                                         default=constants.USER_TYPE_COMMON)
    province = models.CharField('省份', max_length=64, null=True, blank=True)
    city = models.CharField('城市', max_length=64, null=True, blank=True)

    gender = models.SmallIntegerField('性别', choices=GENDER_CHOICES, blank=True, null=True)
    birth = models.DateField('生日', blank=True, null=True)
    channel = models.CharField('渠道', max_length=100, choices=CHANNEL_CHOICES, blank=True, null=True)
    source = models.CharField('当前使用客户端来源', max_length=32, blank=True, null=True,
                              choices=constants.SOURCE_CHOICES)

    version = models.CharField('客户端版本', max_length=100, blank=True, null=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'
        db_table = 'accounts_user_profile'

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    """ 用户地址 """
    user = models.ForeignKey(User, related_name="user_addrs")
    province = models.CharField('省份', max_length=32)
    city = models.CharField('市区', max_length=32)
    area = models.CharField('区域', max_length=32)
    town = models.CharField('街道', max_length=32, null=True, blank=True)

    address = models.CharField('详细地址', max_length=64)
    username = models.CharField('收货人', max_length=32)
    phone = models.CharField('手机号', max_length=32)

    is_default = models.BooleanField('是否为默认地址', default=False)
    is_valid = models.BooleanField('是否有效', default=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户地址'
        verbose_name_plural = '用户地址'
        db_table = 'accounts_user_address'

    @property
    def show_region(self):
        """ 省市区 """
        return '{self.province} {self.city} {self.area}'.format(self=self)

    def show_addr(self):
        return '{self.province} {self.city} {self.area} {self.address} {self.username} {self.phone}'.format(self=self)


class LoginThird(models.Model):
    """ 第三方登录信息 """
    user = models.ForeignKey(User, verbose_name='用户', related_name='third_login', db_index=True)
    login_type = models.SmallIntegerField('登录方式', choices=constants.LOGIN_THIRD_TYPES)
    name = models.CharField('登录账号', max_length=64, db_index=True)
    device = models.CharField('设备型号', max_length=64, null=True, blank=True)
    is_bind = models.BooleanField('是否已经绑定', default=True)
    is_valid = models.BooleanField('是否有效', default=True)
    created_at = models.DateTimeField('用户创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后登陆时间', auto_now=True)

    class Meta:
        verbose_name = '第三方登录信息'
        verbose_name_plural = '第三方登录信息'
        db_table = 'accounts_login_third'


class LoginRecord(models.Model):
    """ 登录记录"""
    user = models.ForeignKey(User, db_index=True, related_name="user_login_records")
    username = models.CharField('登陆账号', max_length=32, db_index=True)
    ip = models.CharField('IP地址', max_length=32, blank=True, null=True)
    address = models.CharField('地址', max_length=100, blank=True, null=True)
    source = models.CharField('来源', max_length=30, blank=True, null=True,
                              choices=constants.SOURCE_CHOICES)
    created_at = models.DateTimeField('登录时间', auto_now_add=True)

    class Meta:
        verbose_name = '登录信息'
        verbose_name_plural = '登录信息'
        db_table = 'accounts_login_record'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return self.__unicode__()


class ChangePasswdLog(models.Model):
    """
    密码改变历史
    """
    user = models.ForeignKey(User, related_name='user_pwd_logs', db_index=True)
    operator = models.ForeignKey(User, verbose_name='操作人', related_name='ope_logs')
    password = models.CharField("密码", max_length=40)
    source = models.CharField('来源', max_length=30, blank=True, null=True,
                              choices=constants.SOURCE_CHOICES)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '密码改变历史记录'
        verbose_name_plural = '密码改变历史记录'
        db_table = 'accounts_password_log'

    def __unicode__(self):
        return '%s' % self.user.username
