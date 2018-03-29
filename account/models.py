from django.db import models
from django.contrib import admin
from django.utils import timezone

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    allowed_count = models.IntegerField()
    last_login_time = models.DateTimeField()
    # 识别身份， 1为普通用户，其它为管理员
    identity = models.IntegerField(default=1)
    # 激活状态
    is_active = models.IntegerField(default=0)


class UserAdmin(admin.ModelAdmin):

    list_display = [
        'username', 'password', 'email', 'allowed_count', 'last_login_time',
        'identity', 'is_active'
    ]


admin.site.register(User, UserAdmin)
