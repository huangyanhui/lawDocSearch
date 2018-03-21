from django.test import TestCase
from django.test import Client
from .models import User
from datetime import datetime
import json

# Create your tests here.
class AccountTest(TestCase):
    # 实例化Client
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Hilary', password='123456', email='654321@163.com', allowed_count=5, last_login_time=datetime.now())

    # 测试用户注册模块
    # 用户注册成功
    def test_user_register_success(self):
        # 设置session
        session = self.client.session
        session['username'] = ''
        session.save()
        # 设置用户注册信息
        data = {'username':'Trump', 'password':'123456', 'email':'123456@163.com'}
        resp = self.client.post('/account/register', data=data)
        content = json.loads(str(resp.content, encoding='utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(content['status'], 'Success')
        self.assertEqual(content['operation'], 'register')
        username = User.objects.filter(username='Trump').first().username
        self.assertEqual(username, 'Trump')

    # 用户邮箱注册信息无效
    def test_user_register_email_invalidate(self):
        # 设置session
        session = self.client.session
        session['username'] = ''
        session.save()
        # 设置用户注册信息，其中邮箱信息无效
        data = {'username':'Obama', 'password':'123456', 'email':'123456@qq。com'}
        resp = self.client.post('/account/register', data=data)
        content = json.loads(str(resp.content, encoding='utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(content['status'], 'Email invalidate')
        self.assertEqual(content['operation'], 'register')

    # 用户名重复
    def test_user_register_exists(self):
        session = self.client.session
        session['username'] = ''
        session.save()
        data = {'username': 'Hilary', 'password': '123456', 'email': '123456@163.com'}
        resp = self.client.post('/account/register', data=data)
        content = json.loads(str(resp.content,encoding='utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(content['status'], 'Username exists.')
        self.assertEqual(content['operation'], 'register')

    # 用户已经登录
    def test_user_register_has_logined(self):
        session = self.client.session
        session['username'] = 'Hilary'
        session.save()
        data = {'username': 'Hilary', 'password': '123456', 'email': '123456@163.com'}
        resp = self.client.post('/account/register', data=data)
        content = json.loads(str(resp.content, encoding='utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(content['status'], 'You are LOGINED.')
        self.assertEqual(content['operation'], 'register')


    # 测试用户登录模块
    def test_user_login_sucess(self):
        session = self.client.session
        session['username'] = ''
        session.save()
        data = {'username': 'Hilary', 'password': '123456', 'email': '123456@163.com'}
        resp = self.client.post('/account/login', data= data)
        content = json.loads(str(resp.content, encoding='utf-8'))
        self.assertEqual(resp.status_code, 200)

    # 测试用户注销模块
    def test_user_logout_success(self):
        session = self.client.session
        session['username'] = 'Hilary'
        session['allowed_count'] = 5
        session['identity'] = 1
        session.save()
        resp = self.client.post('/account/logout')
        self.assertEqual(resp.status_code, 200)
