import calendar # 月末取得用

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import LoginForm, EveryMonthForm
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
    form = EveryMonthForm()
    if request.user.id:
        # lastday変数に月末日の生成
        _, lastday = calendar.monthrange(timezone.now().year, timezone.now().month)
        # 過去から今月末までのデータを取得且つ、今月のみのデータを取得（社員IDを持っている人のみ）
        user_works = Work.objects.order_by("date").filter(
                date__lte=timezone.now().date().replace(day=lastday),
                date__year=form.dates[0][0].split('/')[0],
                date__month=form.dates[0][0].split('/')[1],
                user_id=request.user.id
        )
    else:
        user_works = None
    context = {
            'user_works': user_works,
            'form': form,
    }
    return render(request, 'works/index.html', context)


def pulldown_access(request):
    """
    予約リスト画面のプルダウンによる非同期処理
    メモ：
    プルダウンが押された際に非同期処理としてサクセスされるので、
    返り値をJsonResponseで返し、javascriptの規則でデータが処理されるので、
    Djangoのテンプレートフィルタで簡単に出来ることを以下後半の部分で曜日や時間、コメントの制限を
    実装している。
    コードが汚すぎるしせっかくDjangoを使っているので、テンプレートフィルタが使える方法を今後模索していきたい。
    """
    # javascriptから送られてきた要素を取得
    select_value = request.POST.get("month_val")
    if not select_value:  # 値が存在しなければデフォルトの月別リスト画面を表示
        return redirect("works:index")
    # 「/」に合わせてsplitする
    select_value = select_value.split("/")
    result_query = Work.objects.order_by("date").filter(
        date__year=select_value[0],
        date__month=select_value[1],
    )
    # javascriptでイテレーションするためにリスト内辞書に変換
    query_list = list(result_query.values())
    # 表記を日本人向け（デフォルトのフォーマット）にするため、曜日を設定
    weeks = {
        "Monday": "（月）",
        "Tuesday": "（火）",
        "Wednesday": "（水）",
        "Thursday": "（木）",
        "Friday": "（金）",
        "Saturday": "（土）",
        "Sunday": "（日）",
    }
    # デフォルトのフォーマットに合わせるため、各辞書のキーに代入
    for query in query_list:
        query["date"] = (
            query["date"].strftime("%d")
            + weeks[query["date"].strftime("%A")]
        )
        # 時間データのあるなし処理。ない場合は「null」となるので「''」を代入する
        if query["start_time"]:
            query["start_time"] = query["start_time"].strftime("%H:%M")
        else:
            query["start_time"] = ''
        if query["end_time"]:
            query["end_time"] = query["end_time"].strftime("%H:%M")
        else:
            query["end_time"] = ''
        if query["break_time"]:
            query["break_time"] = query["break_time"].strftime("%H:%M")
        else:
            query["break_time"] = ''
        if len(query["comment"]) >= 40:
            query["comment"] = query["comment"][:40] + '...'
        else:
            pass
    return JsonResponse({"query_list": query_list})


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
