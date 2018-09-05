# -*- coding: utf-8 -*-
__author__ = 'sssssjd'
__date__ = '2018/8/31 14:30'

from django.urls import path, re_path

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView
app_name = 'courses'
urlpatterns = [
    # 课程列表及详情页面的配置
    path('list/', CourseListView.as_view(), name='course_list'),
    re_path('detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    re_path('info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    re_path('comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),

    # 添加课程评论
    path('add_comments/', AddCommentView.as_view(), name='add_comments')
    # re_path('home/(?P<org_id>\d+)/$', CourseListView.as_view(), name='org_home'),
]
