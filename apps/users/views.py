from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm
from utils.email_send import send_register_email
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.get(code=active_code)
        if all_records:
            email = all_records.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
        return render(request, 'login.html', {'msg': '请使用已激活的邮箱登录。'})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_email
            user_profile.email = user_email
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            # 发送邮箱验证码
            send_register_email(user_email, 'register')
            return render(request, 'login.html', {'msg': '请先前往邮箱激活账号再进行登录！'})
        else:
            return render(request, 'register.html', {'register_form': register_form})


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
                    return render(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '该用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})
