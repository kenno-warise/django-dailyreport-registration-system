from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .models import Work


class LoginForm(AuthenticationForm):
    """
    既存の認証用フォームを使用して自作フォームを作成
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
                    }
                ),
                "comment": forms.Textarea(
                    attrs={
                        "class": "form-control",
                        "placeholder": "業務内容",
                        "row": "5",
                    }
                )
        }


class EveryMonthForm(forms.Form):
    """
    月別リストのプルダウン用フォーム
    """
    date = Work.objects.order_by("-date").filter(date__lte=timezone.now().date()).values_list("date")
    date_list = [d[0].strftime("%Y/%m") for d in date]
    date_unique = list(sorted(set(date_list), key=date_list.index))
    date_list_tuple = [(d, d) for d in date_unique]

    dates = tuple(date_list_tuple)

    date_pulldown = forms.ChoiceField(
            choices=dates,
            widget=forms.widgets.Select(
                attrs={"class": "form-select rounded-pill mb-3", "id": "date_pulldown"}
            ),
    )
