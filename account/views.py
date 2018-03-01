from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User

import re


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 已经登录
        if 'allowed_count' in request.session:
            return render(request, 'account/status.html', {
                'operation': 'login',
                'status': 'logined'
            })
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
                    request.session['allowed_count'] = filter_result[
                        0].allowed_count
                    return render(request, 'account/status.html', {
                        'operation': 'login',
                        'status': 'True'
                    })
                # 密码不匹配
                else:
                    return render(request, 'account/status.html', {
                        'operation': 'login',
                        'status': 'Wrong password'
                    })
            # 用户不存在
            else:
                return render(request, 'account/status.html', {
                    'operation': 'login',
                    'status': 'False'
                })
    # 跳转到登录页面
    else:
        return render(request, 'account/login.html')


def logout(request):
    # 已经登录
    if 'allowed_count' in request.session:
        del request.session['allowed_count']
        # 跳转到主页面
        return render(request, 'index.html')
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
        if 'allowed_count' not in request.session:
            username = request.POST['username']
            password = make_password(request.POST['password'])
            print(password)
            email = request.POST['email']
            # 默认查询次数
            allowed_count = 5
            filter_result = User.objects.filter(username=username)
            # 邮箱不合法
            if not validate_email(email):
                return render(request, 'account/status.html', {
                    'operation': 'register',
                    'status': 'Email invalidate'
                })
            # 用户名重复
            elif len(filter_result) != 0:
                return render(request, 'account/status.html', {
                    'operation': 'register',
                    'status': 'Username exists.'
                })
            else:
                new_user = User.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    allowed_count=allowed_count)
                new_user.save()
                return render(request, 'account/status.html', {
                    'operation': 'register',
                    'status': 'Success'
                })
        else:
            return render(request, 'account/status.html', {
                'operation': 'register',
                'status': 'You are LOGINED.'
            })
    else:
        return render(request, 'account/register.html')


def validate_email(email):
    if len(email) > 7:
        if re.match(
                "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                email) != None:
            return True
    return False
