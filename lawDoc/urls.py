from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
url(r'^$', views.index, name='index'),
]
