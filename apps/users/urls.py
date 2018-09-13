# -*- coding: utf-8 -*-
__author__ = 'sssssjd'
__date__ = '2018/9/11 10:27'

from django.urls import path, re_path

from .views import UserInfoView, UploadImageView, ModifyPwdView, SendEmailCodeView,\
    ModifyEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView,\
    MyMessageView

app_name = 'users'
urlpatterns = [
    # user info page
    path('info/', UserInfoView.as_view(), name='user_info'),
    # upload user image
    path('info/upload/', UploadImageView.as_view(), name='image_upload'),
    # modify user password
    path('info/modifypwd/', ModifyPwdView.as_view(), name='modify_password'),
    # modify user email - get email code
    path('send_emailcode/', SendEmailCodeView.as_view(), name='send_emailcode'),
    # modify user email with email code
    path('modify_email/', ModifyEmailView.as_view(), name='modify_email'),

    # user courses
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),

    # user fav
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),

    # user messages
    path('mymessage/', MyMessageView.as_view(), name='mymessage'),

]
