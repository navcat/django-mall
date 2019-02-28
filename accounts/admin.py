from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import UserAddress, User, UserProfile, LoginThird, LoginRecord, ChangePasswdLog


@admin.register(User)
class UserAdmin(UserAdmin):
    """ 用户信息 """
    list_display = ('username', 'nickname', 'is_staff', 'last_login',
                    'date_joined', 'integral', 'level')
    list_per_page = 50
    readonly_fields = ('integral', 'level',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """ 用户详细信息 """
    list_display = ('username', 'user', 'invite_code', 'mobile_no',
                    'user_type',  'channel',
                    'is_mobile_no_verified')
    # readonly_fields = ('user', 'username', 'invite_code')
    search_fields = ('invite_code', 'username', 'user__nickname')
    list_filter = ('user_type', )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """ 用户地址 """
    list_display = ('user', 'province', 'city', 'area',
                    'address', 'username', 'phone', 'is_valid')
    list_filter = ('user__username',)


@admin.register(LoginThird)
class LoginThirdAdmin(admin.ModelAdmin):
    """ 第三方登录关联 """
    list_display = ('user', 'login_type', 'name')
    list_filter = ('user__username',)


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    """ 登录日志 """
    list_display = ('user', 'username', 'ip', 'address', 'source', 'created_at')
    list_filter = ('user__username',)


@admin.register(ChangePasswdLog)
class ChangePasswdLogAdmin(admin.ModelAdmin):
    """ 用户更改密码记录 """
    list_display = ('user', 'operator', 'password', 'source', 'created_at')
    list_filter = ('user__username',)
