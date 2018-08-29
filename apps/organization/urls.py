# -*- coding: utf-8 -*-
__author__ = 'sssssjd'
__date__ = '2018/8/29 16:35'

from django.urls import path, re_path, include

from .views import OrgView, UserAskView

app_name = 'organization'
urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', UserAskView.as_view(), name='user_ask'),
]
