from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    """カスタムユーザーマネージャー"""
    def create_user(self, user_no, password=None):
        if not user_no:
            raise ValueError('社員番号を入力してください。')

        # user = self.model(
        #     email=self.normalize_email(email),
        #)     
        user = self.model(user_no=user_no)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, user_no, password):
        user = self.create_user(
            user_no,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_no, password):
        user = self.create_user(
            user_no,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """カスタムユーザーモデル"""
    user_no = models.CharField(
        verbose_name='社員番号',
        max_length=4,
        help_text="4桁で番号を入力。",
        unique=True,
        error_messages = {
            'unique': '既に使用されている番号です',
        },
        validators=[MinLengthValidator(4)], # 最低の文字数を検証・設定
    )
    username_validators = UnicodeUsernameValidator() # ユーザーネームに関する検証
    username = models.CharField(
            verbose_name='ユーザー名',
            max_length=150,
            help_text="150文字以下の文字や数字、一部の記号で入力してください。",
            validators=[username_validators],
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 
   
    USERNAME_FIELD = 'user_no'

    # User.objectsを呼び出すための変数
    objects = UserManager()

    def __str__(self):             
        return self.user_no


    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    

class Work(models.Model):
    """勤怠情報テーブル"""
    # models.PROTECTによって関連付けられているUserが削除されてもその関連先オブジェクトが存在する限り削除されない
    user_id = models.ForeignKey(User, verbose_name='社員ID', on_delete=models.PROTECT)
    date = models.DateField(verbose_name='日付')
    start_time = models.TimeField(verbose_name='出勤時間')
    end_time = models.TimeField(verbose_name='退勤時間')
    break_time = models.TimeField(verbose_name='休憩時間')
    comment = models.TextField(verbose_name='業務内容')

    def __str__(self):
        return str(self.date)

# Create your models here.
