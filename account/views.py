import base64

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from utils.MyEmail import send_your_email
from .models import User

import re
import json


@csrf_exempt
def login(request):
    if request.method == 'POST':
        response = {'operation': 'login'}
        # 已经登录
        if 'username' in request.session and request.session['username'] != '':
            response['status'] = 'logined'
        # 未登录
        else:
            username = request.POST['username']
            password = request.POST['password']
            # 用户名和密码验证
            user = User.objects.filter(username=username).first()
            # 用户存在
            if user:
                # 已经激活（1为已激活，0为未激活）
                if user.is_active == 1:
                    # 密码匹配
                    if check_password(password, user.password):
                        last_login_time = user.last_login_time
                        now = timezone.now()
                        # 如果大于 1 天，则刷新可查询次数
                        if (now - last_login_time).days >= 1 and user.allowed_count < 5:
                            allowed_count = 5
                        else:
                            allowed_count = user.allowed_count
                        request.session['allowed_count'] = allowed_count
                        request.session['username'] = username
                        # 识别身份（1为普通用户，2为管理员）
                        request.session['identity'] = user.identity
                        # response
                        response['status'] = 'success'
                        response['username'] = username
                        response['allowed_count'] = allowed_count
                        # 密码不匹配
                    else:
                        response['status'] = 'wrong password'
                else:
                    response['status'] = 'not actived'
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
        # request.session['allowed_count'] = 99999999999999
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
            username_filter_result = User.objects.filter(username=username)
            email_filter_result = User.objects.filter(email=email)
            # 邮箱不合法
            if not validate_email(email):
                response['status'] = 'Email invalidate'
            # 邮箱重复
            elif len(email_filter_result) != 0:
                response['status'] = 'Email exists.'
            # 用户名重复
            elif len(username_filter_result) != 0:
                response['status'] = 'Username exists.'
            else:
                # url = 'http://' + request.get_host() + '/account/active/'
                url = 'http://yaexp.com/account/active/'
                if send_your_email(email, username, url, 'register') == 1:
                    new_user = User.objects.create(
                        username=username,
                        password=password,
                        email=email,
                        allowed_count=allowed_count,
                        last_login_time=timezone.now(),
                        identity=1,
                        is_active=0)
                    new_user.save()
                    response['status'] = 'Success'
                else:
                    response['status'] = 'Failed to send email'
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


@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        response = {'operation': 'forget_password'}
        # 已经登录
        if request.session['username'] != '':
            response['status'] = 'logined'
        # 未登录
        else:
            username = request.POST['username']
            email = request.POST['email']
            filter_result = User.objects.filter(username=username)
            # 邮箱不合法
            if not validate_email(email):
                response['status'] = 'Email invalidate'
            # 用户名重复
            elif len(filter_result) == 0:
                response['status'] = 'Username unexists.'
            else:
                # url = 'http://' + request.get_host() + '/account/reset/'
                url = 'http://yaexp.com/account/reset/'
                print(url)
                # 邮箱匹配
                if email == filter_result[0].email:
                    if send_your_email(email, username, url,
                                       'forget_password') == 1:
                        response['status'] = 'Success'
                    else:
                        response['status'] = 'try again'
                else:
                    response['status'] = 'Wrong email'
        print(response['status'])
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        return render(request, 'account/forget_password.html')


@csrf_exempt
def reset(request, code):
    if request.method == 'GET':
        return render(request, 'account/reset.html')
    if request.method == 'POST':
        # url解密
        code = code + '\n'
        code = code.encode('utf-8')
        code = base64.decodebytes(code).decode('utf-8')
        name = code.split('##')[0]
        print(name)
        # 验证url是否合法
        filter_result = User.objects.filter(username=name)
        # 如果地址非法，返回主页
        if filter_result == 0:
            return render(request, 'index.html')
        # 地址合法，验证两次密码是否相同
        else:
            response = {'operation': 'reset'}
            if request.POST['password'] == request.POST['re-password']:
                try:
                    # 修改密码
                    password = request.POST['password']
                    user = User.objects.get(username=name)
                    user.password = make_password(password)
                    user.save()
                    response['status'] = 'Sucess'
                except Exception as e:
                    # 查询错误
                    print(e)
                    print('查询错误')
                    response['status'] = 'query error'
            else:
                # 两次输入密码不同
                response['status'] = 'email error'
        print(response['status'])
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@csrf_exempt
def active(request, code):
    code = code + '\n'
    code = code.encode('utf-8')
    code = base64.decodebytes(code).decode('utf-8')
    username = code.split('##')[0]

    user = User.objects.filter(username=username).first()

    user.is_active = 1
    user.save()

    return render(request, 'account/login.html')
