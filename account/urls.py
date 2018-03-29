from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('forget_password', views.forget_password, name='forget_password'),
    url('reset/(?P<code>.*)', views.reset, name='reset'),
    url('active/(?P<code>.*)', views.active, name='active'),
]
