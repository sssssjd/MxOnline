# -*- coding: utf-8 -*-
__author__ = 'sssssjd'
__date__ = '2018/8/29 16:35'

from django.urls import path, re_path, include

from .views import OrgView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView

app_name = 'organization'
urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', UserAskView.as_view(), name='user_ask'),
    re_path('home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    re_path('course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    re_path('desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    re_path('teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
]
