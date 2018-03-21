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


def send_your_email(email, send_type='foget_password'):
    code = generate_random_str(4)
    email_title = '换宴会'
    email_body = '请点击下面的链接修改你的密码: http://127.0.0.1:8000/active/{0}'.format(code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return send_status
