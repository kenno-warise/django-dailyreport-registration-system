import calendar # 月末取得用

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import LoginForm, WorkForm, EveryMonthForm
from .models import Work, User


class Login(LoginView):
    """ログイン画面"""
    form_class = LoginForm
    template_name = "works/login.html"
    redirect_authenticated_user = True # ログイン状態で/login/にアクセスされた時にリダイレクト先へ飛ばす


class Logout(LogoutView):
    """ログアウト"""

@login_required(login_url='/login/')
def index(request):
    """
    日報登録＆月別リスト画面
    """
    this_month_check = Work.objects.filter(user_id=request.user.id, date=timezone.now().date())
    if not this_month_check: # 今月のデータが空だった場合自動で作成する
        _, lastday = calendar.monthrange(timezone.now().year, timezone.now().month)
        for i in range(lastday):
            t = timezone.now().date().replace(day=1) + timezone.timedelta(days=i)
            Work.objects.create(user_id=User.objects.get(id=request.user.id), date=t.strftime('%Y-%m-%d'))
    # プルダウン用のフォームだっけかな？
    form = EveryMonthForm()

    # ログインしないとアクセスできないので次期要らな処理となる
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
    if request.method == "POST":
        post_data = request.POST
        # 新たにPOSTされたデータを使用して更新用データを取得
        edit_work = get_object_or_404(
                Work,
                user_id=post_data['user_id'],
                date=post_data['date']
        )
        modal_form = WorkForm(request.POST, instance=edit_work)
        if modal_form.is_valid():
            modal_form.save()
            return redirect('works:index')
    
    work = get_object_or_404(Work, user_id=request.user.id, date=timezone.now().date().strftime("%Y-%m-%d"))
    modal_form = WorkForm(instance=work)
    context = {
            'user_works': user_works,
            'form': form,
            'modal_form': modal_form,
            'work': work,
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
    コードが汚すぎるしせっかくDjangoを使っているので、テンプレートフィルタが使える方法を今後模索していく。
    """
    # javascriptから送られてきた要素を取得
    select_value = request.POST.get("month_val")
    if not select_value:  # 値が存在しなければデフォルトの月別リスト画面を表示
        return redirect("works:index")
    # 「/」に合わせてsplitする
    select_value = select_value.split("/")
    result_query = Work.objects.order_by("date").filter(
        user_id=request.user.id, # 社員画面ではログイン中のidを参照
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
        query["week"] = (
            query["date"].strftime("%d")
            + weeks[query["date"].strftime("%A")]
        )
        # 時間データのあるなし処理。ない場合は「null」となるので「''」を代入する
        if query["start_time"]:
            query["start_time"] = query["start_time"].strftime("%H:%M")
        else:
            query["start_time"] = ' '
        if query["end_time"]:
            query["end_time"] = query["end_time"].strftime("%H:%M")
        else:
            query["end_time"] = ' '
        if query["break_time"]:
            query["break_time"] = query["break_time"].strftime("%H:%M")
        else:
            query["break_time"] = ' '
        if query["comment"]:
            if len(query["comment"]) >= 40:
                query["comment"] = query["comment"][:40] + '...'
            else:
                pass
        else:
            query["comment"] = ' '

    return JsonResponse({"query_list": query_list})


class AdminLogin(LoginView):
    """管理者ログイン画面"""
    form_class = LoginForm
    template_name = "works/admin_login.html"
    redirect_authenticated_user = True # ログイン状態で/admin-login/にアクセスされた時にリダイレクト先へ飛ばす
    redirect_field_name = 'user-list' # リダイレクトり先が「/admin-login/user-list/」となる

    def form_invalid(self, form):
        """検証失敗後の処理"""
        # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
        auth_result = authenticate(username=form.data['username'], password=form.data['password'])
        # 管理者かどうかのブール値を出力するための変数
        user = User.objects.filter(user_no=form.data['username']).values_list('admin')
        for field in form:
            if field.errors:
                # フォームが未入力のフィールド
                # 入力されていないフィールドはclass属性にis-invalidを追記する
                form[field.name].field.widget.attrs["class"] += " is-invalid"
            elif auth_result is None:
                # 認証に失敗したらinvalid
                form[field.name].field.widget.attrs["class"] += " is-invalid"
            elif user.get()[0] is False:
                # 管理者でなければinvalid
                form[field.name].field.widget.attrs["class"] += " is-invalid"
        
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_redirect_url(self):
        """
        フォームの認証、検証共に成功した後の処理
        リダイレクト先の戻り値指定
        """
        redirect_to = self.redirect_field_name
        return redirect_to
    
    def post(self, request, *args, **kwargs):
        """
        POSTパラメータを押された際の処理
        管理者でなければ無効にする
        """
        form = self.get_form()
        auth_result = authenticate(username=form.data['username'], password=form.data['password'])
        user = User.objects.filter(user_no=form.data['username']).values_list('admin')
        if auth_result: # 認証されれば成功
            if user.get()[0]: # 管理者かどうか
                if form.is_valid(): # フォームデータの検証
                    return self.form_valid(form)
                else:
                    return self.form_invalid(form)
        return self.form_invalid(form)


@login_required(login_url='/admin-login/')
def user_list(request):
    """社員一覧"""
    if request.user.admin is False:
        return redirect('works:index')
    users = User.objects.all()
    context = {
            'users': users
    }
    return render(request, 'works/user_list.html', context)


@login_required(login_url='/admin-login/')
def user_result(request, user_id):
    """日報登録＆月別リスト"""
    form = EveryMonthForm()
    work = get_object_or_404(Work, user_id=user_id, date=timezone.now().date().strftime("%Y-%m-%d"))
    # work = Work.objects.filter(user_id=request.user.id, date=timezone.now().date().strftime("%Y-%m-%d"))
    modal_form = WorkForm(instance=work)
    if request.user.id:
        # リスト表示用のデータ生成
        # lastday変数に月末日の生成
        _, lastday = calendar.monthrange(timezone.now().year, timezone.now().month)
        # 過去から今月末までのデータを取得且つ、今月のみのデータを取得（社員IDを持っている人のみ）
        user_works = Work.objects.order_by("date").filter(
                date__lte=timezone.now().date().replace(day=lastday),
                date__year=form.dates[0][0].split('/')[0],
                date__month=form.dates[0][0].split('/')[1],
                user_id=user_id
        )
    else:
        user_works = None
    if request.method == "POST":
        post_data = request.POST
        # 新たにPOSTされたデータを使用して更新用データを取得
        edit_work = get_object_or_404(
                Work,
                user_id=user_id,
                date=post_data['date']
        )
        modal_form = WorkForm(request.POST, instance=edit_work)
        if modal_form.is_valid():
            modal_form.save()
            return redirect('works:user-result', user_id)
    context = {
            'user_works': user_works,
            'form': form,
            'modal_form': modal_form,
            'work': work,
    }
    return render(request, 'works/user_result.html', context)

# Create your views here.
