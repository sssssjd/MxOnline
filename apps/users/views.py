import json
from pure_pagination import Paginator, PageNotAnInteger

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 注册用户激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html', {'msg': '请使用已激活的邮箱登录。'})


# 用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_email):
                return render(request, 'register.html', {'msg': '用户已存在！', 'register_form': register_form})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_email
            user_profile.email = user_email
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            # 写入欢迎注册信息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕学在线网'
            user_message.save()

            # 发送邮箱验证码
            send_register_email(user_email, 'register')
            return render(request, 'login.html', {'msg': '请先前往邮箱激活账号再进行登录！'})
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 用户登录
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '该用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 用户退出登录
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 忘记密码页面
class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


# 重置密码页面1
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# 重置密码页面2
class ResetPwdView(View):
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'resetpwd_form': resetpwd_form})


# user info
class UserInfoView(LoginRequiredMixin, View):
    """
    userinfo - page
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# upload user image
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ModifyPwdView(View):
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"两次输入的密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(resetpwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'modify_email')
        return HttpResponse('{"status":"success", "email":"验证码已发送"}', content_type='application/json')


class ModifyEmailView(LoginRequiredMixin, View):
    """
    modify user email with email code
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='modify_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    user courses in usercenter
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {'user_courses': user_courses})


class MyFavOrgView(LoginRequiredMixin, View):
    """
    user fav org in usercenter
    """
    def get(self, request):
        fav_org_list = []
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for user_fav_org in user_fav_orgs:
            org_id = user_fav_org.fav_id
            org = CourseOrg.objects.get(id=int(org_id))
            fav_org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'fav_org_list': fav_org_list})


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    user fav teacher in usercenter
    """
    def get(self, request):
        fav_teacher_list = []
        user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for user_fav_teacher in user_fav_teachers:
            teacher_id = user_fav_teacher.fav_id
            teacher = Teacher.objects.get(id=int(teacher_id))
            fav_teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {'fav_teacher_list': fav_teacher_list})


class MyFavCourseView(LoginRequiredMixin, View):
    """
    user fav course in usercenter
    """
    def get(self, request):
        fav_course_list = []
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for user_fav_course in user_fav_courses:
            course_id = user_fav_course.fav_id
            course = Course.objects.get(id=int(course_id))
            fav_course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'fav_course_list': fav_course_list})


class MyMessageView(LoginRequiredMixin, View):
    """
    user messages
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = all_messages.filter(has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 对消息分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, per_page=3)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'messages': messages})


class IndexView(View):
    def get(self, request):
        # banner
        all_banners = Banner.objects.all().order_by('index')
        # Course
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        courses = Course.objects.filter(is_banner=False)[:5]

        # Org
        orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'banner_courses': banner_courses,
            'courses': courses,
            'orgs': orgs,
        })


# 404 page
def page_not_found(request, **kwargs):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 403 page
def page_forbidden(request, **kwargs):
    from django.shortcuts import render_to_response
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response


# 500 page
def page_error(request, **kwargs):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
