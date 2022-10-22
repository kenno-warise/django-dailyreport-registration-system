from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import LoginForm

"""
class Login(LoginView):
    ログイン画面
    form_class = LoginForm
    template_name = "works/login.html"
"""

def login(request):
    """
    タスク↓↓
    入力値を取得、入力値をチェック 〇
    データベースに照合
    セッションに保存、HOME画面へ遷移
    """
    if request.POST:
        print()
        print(request.POST)
        user_no = request.POST['user_no']
        password = request.POST['password']
        # if request.user.is_authennticated:
        if user_no and password:
            return redirect('works:index')
        else:
            context = {
                    'user_no': user_no,
                    'password': password,
            }
            return render(request, 'works/login.html', context)
    return render(request, 'works/login.html')

# ログインリダイレクト先の設定をする
# @login_required(login_url='/login/')
def index(request):
    return render(request, 'works/index.html')


def admin_login(request):
    return render(request, 'works/admin_login.html')


def user_list(request):
    return render(request, 'works/user_list.html')


def user_result(request):
    return render(request, 'works/user_result.html')

# Create your views here.
