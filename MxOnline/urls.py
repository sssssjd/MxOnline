"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin
from MxOnline.settings import MEDIA_ROOT
from MxOnline.settings import STATIC_ROOT
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView,\
    ResetView, ResetPwdView, LogoutView, IndexView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    path('forgetpwd/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd_get'),
    path('resetpwd/', ResetPwdView.as_view(), name='reset_pwd_post'),

    # 课程机构url配置
    path('org/', include('organization.urls', namespace='org')),

    # 课程相关url配置
    path('course/', include('courses.urls', namespace='course')),

    # 用户信息相关url配置
    path('user/', include('users.urls', namespace='user')),

    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # Uedit富文本编辑器
    re_path(r'^ueditor/', include('DjangoUeditor.urls'))

]

handler404 = 'users.views.page_not_found'
handler403 = 'users.views.page_forbidden'
handler500 = 'users.views.page_error'

