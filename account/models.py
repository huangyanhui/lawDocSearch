from django.db import models
from django.contrib import admin

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    allowed_count = models.IntegerField()


class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'password', 'email', 'allowed_count']


admin.site.register(User, UserAdmin)
