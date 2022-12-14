from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EveryMonthForm, LoginForm, WorkForm
from .functions import create_user_works, month_check
from .models import User, Work


class Login(LoginView):
    """ログイン画面"""

    form_class = LoginForm
    template_name = "works/login.html"
    redirect_authenticated_user = True  # ログイン状態で/login/にアクセスされた時にリダイレクト先へ飛ばす

    def form_invalid(self, form):
        """検証失敗後の処理"""
        # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
        auth_result = authenticate(
            username=form.data["username"], password=form.data["password"]
        )
        # 管理者かどうかのブール値を出力するための変数
        user = User.objects.filter(user_no=form.data["username"]).values_list("admin")
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


class Logout(LogoutView):
    """ログアウト"""

    template_name = "works/index"


# 一般ユーザーが直接アクセスしてきた際にログイン画面へとリダイレクトされるようにする
@login_required(login_url="/login/")
def index(request):
    """
    日報登録＆月別リスト画面
    """

    # 最新の月データが存在するかチェック用の関数
    month_check(request.user.id)

    # 当月の勤怠情報を表示するためのデータを取得
    user_works = create_user_works(request.user.id)

    # モーダルの更新用フォームとして使用するクエリ
    work = get_object_or_404(
        Work, user_id=request.user.id, date=timezone.now().date().strftime("%Y-%m-%d")
    )
    # モーダルフォームの作成
    modal_form = WorkForm(instance=work)
    if request.method == "POST":
        """
        モーダルがポストされた時の処理
        """
        # 新たにPOSTされたデータを使用して更新用データを取得
        work = get_object_or_404(
            Work,
            # データの取得に必要なユーザーID
            user_id=request.POST["user_id"],
            # POSTされた日付を割り当てる
            date=request.POST["date"],
        )
        modal_form = WorkForm(request.POST, instance=work)
        if modal_form.is_valid():  # 検証成功した場合
            if modal_form.initial["start_time"]:  # 出勤データが既にある場合は退勤フォームをテスト
                """
                カスタムユーザーを使っているため、バリデーションエラー等の
                エラーメッセージやvalidatoreの実装のしかたが分からないので
                各フォームを１つずつテストをしてエラーを出している
                """
                if modal_form.initial["end_time"]:  # 退勤データが既にある場合は休憩フォームをテスト
                    if modal_form.data["break_time"]:  # 休憩フォームに入力されている場合はセーブでリダイレクト
                        modal_form.save()
                        return redirect("works:index")
                    else:  # 休憩フォームが未入力だった場合はエラー
                        modal_form["break_time"].field.widget.attrs[
                            "class"
                        ] += " is-invalid"
                else:
                    if modal_form.data["end_time"]:  # 退勤フォームが入力されている場合はセーブでリダイレクト
                        modal_form.save()
                        return redirect("works:index")
                    else:  # 退勤フォームが未入力だった場合はエラー
                        modal_form["end_time"].field.widget.attrs[
                            "class"
                        ] += " is-invalid"

            else:  # 出勤データが無かった場合
                if modal_form.data["start_time"]:  # 出勤フォームに入力されている場合はセーブでリダイレクト
                    modal_form.save()
                    return redirect("works:index")
                else:  # 出勤フォームが入力されていなかった場合エラー
                    modal_form["start_time"].field.widget.attrs[
                        "class"
                    ] += " is-invalid"
        else:  # 検証失敗でフォームが未入力だった場合
            for field in modal_form:
                if field.errors:
                    # フォームが未入力のフィールド
                    # 入力されていないフィールドはclass属性にis-invalidを追記する
                    modal_form[field.name].field.widget.attrs["class"] += " is-invalid"

    # 月で切り替えるためのプルダウンフォーム
    pulldown_form = EveryMonthForm()

    context = {
        "user_works": user_works,
        "pulldown_form": pulldown_form,
        "modal_form": modal_form,
        "work": work,
    }
    return render(request, "works/index.html", context)


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
        user_id=request.user.id,  # 社員画面ではログイン中のidを参照
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
            query["date"].strftime("%d") + weeks[query["date"].strftime("%A")]
        )
        # 時間データのあるなし処理。ない場合は「null」となるので「''」を代入する
        if query["start_time"]:
            query["start_time"] = query["start_time"].strftime("%H:%M")
        else:
            query["start_time"] = " "
        if query["end_time"]:
            query["end_time"] = query["end_time"].strftime("%H:%M")
        else:
            query["end_time"] = " "
        if query["break_time"]:
            query["break_time"] = query["break_time"].strftime("%H:%M")
        else:
            query["break_time"] = " "
        if query["comment"]:
            if len(query["comment"]) >= 40:
                query["comment"] = query["comment"][:40] + "..."
            else:
                pass
        else:
            query["comment"] = " "

    return JsonResponse({"query_list": query_list})


class AdminLogin(LoginView):
    """管理者ログイン画面"""

    form_class = LoginForm
    template_name = "works/admin_login.html"
    redirect_authenticated_user = True  # ログイン状態で/admin-login/にアクセスされた時にリダイレクト先へ飛ばす
    redirect_field_name = "user-list"  # リダイレクトり先が「/admin-login/user-list/」となる

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
        if form.is_valid():  # フォームの検証
            auth_result = authenticate(
                username=form.data["username"], password=form.data["password"]
            )
            if auth_result:  # 認証されれば成功
                user = User.objects.filter(user_no=form.data["username"]).values_list(
                    "admin"
                )
                if user.get()[0]:  # 管理者かどうか
                    return self.form_valid(form)
                else:
                    # 管理者以外だった場合のエラーメッセージ
                    form.add_error("username", "認証に失敗しました。")
                    return self.form_invalid(form)
            else:  # 認証されなければ失敗
                return self.form_invalid(form)

        return self.form_invalid(form)

    def form_invalid(self, form):
        """検証失敗後の処理"""
        # 各フィールドのclass属性にis-invalid（失敗）もしくわis-valid（クリア）を追記する
        auth_result = authenticate(
            username=form.data["username"], password=form.data["password"]
        )
        # 管理者かどうかのブール値を出力するための変数
        user = User.objects.filter(user_no=form.data["username"]).values_list("admin")
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


@login_required(login_url="/admin-login/")
def user_list(request):
    """社員一覧"""
    if request.user.admin is False:
        return redirect("works:index")
    users = User.objects.all()
    context = {"users": users}
    return render(request, "works/user_list.html", context)


@login_required(login_url="/admin-login/")
def user_result(request, user_id):
    """日報登録＆月別リスト"""

    # 最新の月データが存在するかチェック用の関数
    month_check(user_id)

    # 当月の勤怠情報を表示するためのデータを取得
    user_works = create_user_works(user_id)

    work = get_object_or_404(
        Work, user_id=user_id, date=timezone.now().date().strftime("%Y-%m-%d")
    )
    modal_form = WorkForm(instance=work)
    if request.method == "POST":
        post_data = request.POST
        # 新たにPOSTされたデータを使用して更新用データを取得
        edit_work = get_object_or_404(Work, user_id=user_id, date=post_data["date"])
        modal_form = WorkForm(request.POST, instance=edit_work)
        if modal_form.is_valid():
            modal_form.save()
            return redirect("works:user-result", user_id)

    # 月で切り替えるためのプルダウンフォーム
    pulldown_form = EveryMonthForm()

    context = {
        "user_works": user_works,
        "pulldown_form": pulldown_form,
        "modal_form": modal_form,
        "work": work,
    }
    return render(request, "works/user_result.html", context)


# Create your views here.
