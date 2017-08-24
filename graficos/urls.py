"""impressoes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'upload/', views.cvs_upload, name='upload'),
    url(r'report/(?P<cooperativa>[0-9]+)/(?P<pa>[0-9]+)/(?P<ano>[0-9]+)/(?P<mes>[0-9]+)/$', views.report, name='report'),
    url(r'plot/(?P<cooperativa>[0-9]+)/(?P<pa>[0-9]+)/(?P<ano>[0-9]+)/(?P<mes>[0-9]+)/(?P<tipo>[a-zA-Z]+)/$', views.plot, name='plot'),
]
