from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm
from .models import Work


class Login(LoginView):
    """ログイン画面"""
    form_class = LoginForm
    template_name = "works/login.html"
    redirect_authenticated_user = True # ログイン状態で/login/にアクセスされた時にリダイレクト先へ飛ばす


class Logout(LogoutView):
    """ログアウト"""

@login_required(login_url='/login/')
def index(request):
    """日報登録＆月別リスト画面"""
    if request.user.id:
        user_works = Work.objects.filter(user_id=request.user.id)
    else:
        user_works = None
    context = {
            'user_works': user_works,
    }
    # リクエストされてきた社員IDからそのIDのデータベースから値を取得できているか確認
    print()
    print(user_works)
    return render(request, 'works/index.html', context)


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
