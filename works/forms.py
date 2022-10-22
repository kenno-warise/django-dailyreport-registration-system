from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control rounded-pill"
        self.fields["username"].widget.attrs["placeholder"] = "社員番号"
        self.fields["password"].widget.attrs["class"] = "form-control rounded-pill"
        self.fields["password"].widget.attrs["placeholder"] = "パスワード"
