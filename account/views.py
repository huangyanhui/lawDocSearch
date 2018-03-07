from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import User

import re
import json


@csrf_exempt
def login(request):
    if request.method == 'POST':
        response = {'operation': 'login'}
        # 已经登录
        if 'allowed_count' in request.session:
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
                    allowed_count = filter_result[0].allowed_count
                    request.session['allowed_count'] = allowed_count
                    request.session['username'] = username
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
    if 'allowed_count' in request.session:
        del request.session['allowed_count']
        del request.session['username']
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
        response = {'operation':'register'}
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
                response['status'] = 'Email invalidate'
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            # 用户名重复
            elif len(filter_result) != 0:
                response['status'] = 'Username exists.'
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            else:
                new_user = User.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    allowed_count=allowed_count)
                new_user.save()
                response['status'] = 'Success'
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response['status'] = 'You are LOGINED.'
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        return render(request, 'account/register.html')


def validate_email(email):
    if len(email) > 7:
        if re.match(
                "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                email) != None:
            return True
    return False
