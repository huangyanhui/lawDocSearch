from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import User

import re
import json


@csrf_exempt
def login(request):
    if request.method == 'POST':
        response = {'operation': 'login'}
        # 已经登录
        if request.session['username'] != '':
            response['status'] = 'logined'
        # 未登录
        else:
            username = request.POST['username']
            password = request.POST['password']
            # 用户名和密码验证
            filter_result = User.objects.filter(username=username)
            # 用户存在
            if len(filter_result) > 0:
                # 密码匹配
                if check_password(password, filter_result[0].password):
                    last_login_time = filter_result[0].last_login_time
                    now = timezone.now()
                    # 如果大于 1 天，则刷新可查询次数
                    if (now - last_login_time).days >= 1:
                        allowed_count = 5
                    else:
                        allowed_count = filter_result[0].allowed_count
                    request.session['allowed_count'] = allowed_count
                    request.session['username'] = username
                    # 识别身份（1为普通用户，2为管理员）
                    request.session['identity'] = filter_result[0].identity
                    # response
                    response['status'] = 'success'
                    response['username'] = username
                    response['allowed_count'] = allowed_count
                # 密码不匹配
                else:
                    response['status'] = 'wrong password'
            # 用户不存在
            else:
                response['status'] = 'user did not existed'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    # 跳转到登录页面
    else:
        return render(request, 'account/login.html')


def logout(request):
    # 已经登录
    if request.session['username'] != '':
        user = User.objects.get(username=request.session['username'])
        user.allowed_count = request.session['allowed_count']
        user.last_login_time = timezone.now()
        user.save()
        request.session['username'] = ''
        # 登出后默认没有搜索次数
        # request.session['allowed_count'] = -1
        # DEBUG 语句
        request.session['allowed_count'] = 99999999999999
        # DEBUG 语句
        # 删除识别身份
        del request.session['identity']
        # 跳转到主页面
        return render(
            request, 'index.html', {
                'username': request.session['username'],
                'allowed_count': request.session['allowed_count'],
                'identity': 1,
            })
    # 未登录
    else:
        return render(request, 'account/status.html', {
            'operation': 'logout',
            'status': 'You are not LOGIN'
        })


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 未登录
        response = {'operation': 'register'}
        if request.session['username'] == '':
            username = request.POST['username']
            password = make_password(request.POST['password'])
            email = request.POST['email']
            # 默认查询次数
            allowed_count = 5
            filter_result = User.objects.filter(username=username)
            # 邮箱不合法
            if not validate_email(email):
                response['status'] = 'Email invalidate'
            # 用户名重复
            elif len(filter_result) != 0:
                response['status'] = 'Username exists.'
            else:
                new_user = User.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    allowed_count=allowed_count,
                    last_login_time=timezone.now(),
                    identity=1)
                new_user.save()
                response['status'] = 'Success'
        else:
            response['status'] = 'You are LOGINED.'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        return render(request, 'account/register.html')


def validate_email(email):
    if len(email) > 7:
        if re.match(
                "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                email):
            return True
    return False
