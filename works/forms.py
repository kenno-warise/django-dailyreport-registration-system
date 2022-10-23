from django import forms
from django.contrib.auth.forms import AuthenticationForm


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


