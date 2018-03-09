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


class UserAdmin(admin.ModelAdmin):

    list_display = [
        'username', 'password', 'email', 'allowed_count', 'last_login_time'
    ]


admin.site.register(User, UserAdmin)
