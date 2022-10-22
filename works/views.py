from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from .forms import LoginForm


class Login(LoginView):
    """ログイン画面"""
    form_class = LoginForm
    template_name = "works/login.html"
    redirect_authenticated_user = True # ログイン状態で/login/にアクセスされた時にリダイレクト先へ飛ばす


class Logout(LogoutView):
    """ログアウト"""


def index(request):
    """日報登録＆月別リスト画面"""
    return render(request, 'works/index.html')


def admin_login(request):
    """管理者ログイン画面"""
    return render(request, 'works/admin_login.html')


def user_list(request):
    """社員一覧"""
    return render(request, 'works/user_list.html')


def user_result(request):
    """日報登録＆月別リスト"""
    return render(request, 'works/user_result.html')

# Create your views here.
