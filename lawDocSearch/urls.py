"""lawDocSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from lawDoc.views import index, indexSearch, getDetail, download, groupBySearch, addSearch, getMore, newSearch, \
    searchlabel, getRecommond, getRecommondList

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^indexsearch$', indexSearch),
    url(r'^searchresult$', getDetail, name="getDetail"),
    url(r'^addsearchandterm$', groupBySearch, name="addsearchandterm"),
    url(r'^getmore$',getMore, name="getmore"),
    url(r'^addsearch$', addSearch, name="addSearch"),
    url(r'^download$', download, name="download"),
    url(r'^newsearch$', newSearch, name="newSearch"),
    url(r'^searchlabel$', searchlabel, name="searchlabel"),
    url(r'^recommondDetail$',getRecommond,name='getRecommond'),
    url(r'^recommondList$',getRecommondList,name='getRecommondLsit'),
    path('account/', include('account.urls')),
    path('upload/', include('upload.urls')),
]
