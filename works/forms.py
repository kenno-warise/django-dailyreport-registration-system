from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .models import Work, User


class LoginForm(AuthenticationForm):
    """
    既存の認証用フォームを使用して自作フォームを作成
    メモ：
    カスタムユーザーフィールドで定義したヘルプテキストや
    バリデーションエラー等のメッセージがこの継承クラスに
    反映されていないようなので、時間がある時に公式ドキュメントを
    見直す。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # カスタムユーザーモデルは「user_no」を認証にしているが、ここでは「user_no」が「username」としてキーになっている
        self.fields["username"].widget.attrs["class"] = "form-control rounded-pill"
        self.fields["username"].widget.attrs["placeholder"] = "社員番号"
        self.fields["password"].widget.attrs["class"] = "form-control rounded-pill"
        self.fields["password"].widget.attrs["placeholder"] = "パスワード"


class WorkForm(forms.ModelForm):
    """モーダル用のフォーム"""

    class Meta:
        model = Work
        fields = (
                'user_id',
                'date',
                'start_time',
                'end_time',
                'break_time',
                'comment',
        )
        widgets = {
                "user_id": forms.NumberInput(
                    attrs={
                        "id": "modal_user_id",
                        "name": "modal_user_id",
                    }
                ),
                "date": forms.TextInput(
                    attrs={
                        "id": "modal_date",
                        "name": "modal_date",
                    }
                ),
                "start_time": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "出勤",
                        "id": "modal_start_time",
                        "name": "modal_start_time",
                    }
                ),
                "end_time": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "退勤",
                        "id": "modal_end_time",
                        "name": "modal_end_time",
                    }
                ),
                "break_time": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "休憩",
                        "id": "modal_break_time",
                        "name": "modal_break_time",
                    }
                ),
                "comment": forms.Textarea(
                    attrs={
                        "class": "form-control",
                        "placeholder": "業務内容",
                        "id": "modal_comment",
                        "name": "modal_comment",
                        "row": "5",
                    }
                )
        }


class EveryMonthForm(forms.Form):
    """
    月別リストのプルダウン用フォーム
    """
    # 本日までのデータを取得（未来のデータを取得しないため）
    date = Work.objects.order_by("-date").filter(date__lte=timezone.now().date()).values_list("date")
    # 年/月に変換し保管
    date_list = [d[0].strftime("%Y/%m") for d in date]
    # 上記のorder_by("-date")の並び順を固定で、リストのindex番号12番目までを取得（過去１２か月分）
    date_unique = list(sorted(set(date_list), key=date_list.index))[:12]
    # choicesに渡すため要素をタプルで囲み一時保管
    date_list_tuple = [(d, d) for d in date_unique]
    # リストからタプルにして準備完了
    dates = tuple(date_list_tuple)

    date_pulldown = forms.ChoiceField(
            choices=dates,
            widget=forms.widgets.Select(
                attrs={"class": "form-select rounded-pill mb-3", "id": "date_pulldown"}
            ),
    )
