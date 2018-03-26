import base64
import time

from random import Random
from django.core.mail import send_mail

from lawDocSearch.settings import EMAIL_FROM


def generate_random_str(random_length=4):
    random_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkIiMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        random_str += chars[random.randint(0, length)]
    return random_str


def send_your_email(email, name, url, send_type):
    ticks = time.time()
    s1 = name + '##' + str(ticks)
    # 以时间戳作为加密附加内容
    s2 = base64.encodebytes(s1.encode('utf-8')).decode('utf-8')[:-1]

    if send_type == 'forget_password':
        email_title = '换密码'
        email_body = '请点击下面的链接修改你的密码: ' + url + '{0}'.format(s2)
    elif send_type == 'register':
        email_title = '确定注册'
        email_body = '请点击下面的链接确定注册: ' + url + '{0}'.format(s2)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return send_status
