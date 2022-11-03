import calendar

from django.core.signing import Signer
from django.utils import timezone

from . import models


def create_user_works(user_id):
    """
    当月の勤怠情報を表示するための関数
    使用場所：views.py(月別リスト画面、管理者用月別リスト)
    """
    # lastday変数に月末日の生成
    _, lastday = calendar.monthrange(timezone.now().year, timezone.now().month)
    # 過去から今月末までのデータを取得且つ、今月のみのデータを取得（社員IDを持っている人のみ）
    user_works = models.Work.objects.order_by("date").filter(
            date__gte=timezone.now().date().replace(day=1),
            date__lte=timezone.now().date().replace(day=lastday),
            user_id=user_id
    )
    return user_works


def month_check(user_id):
    """
    最新の月データチェック用の共通関数
    使用場所：views.py(月別リスト画面、管理者用月別リスト)
    """
    this_month_check = models.Work.objects.filter(user_id=user_id, date=timezone.now().date())
    if not this_month_check: # 今月のデータが空だった場合自動で作成する
        _, lastday = calendar.monthrange(timezone.now().year, timezone.now().month)
        for i in range(lastday):
            t = timezone.now().date().replace(day=1) + timezone.timedelta(days=i)
            models.Work.objects.create(user_id=models.User.objects.get(id=user_id), date=t.strftime('%Y-%m-%d'))


def encryption(target):
    """
    暗号化
    使用場所：models.py(カスタムユーザーのSaveメソッド)
    """
    signer = Signer() # keyはデフォルトの「SECRET_KEY」を使用
    value = signer.sign(target)
    value_list = [value.split(':')]
    dict_sign = dict(value_list)
    signed_obj = signer.sign_object(dict_sign)
    return signed_obj


def decryption(target):
    """
    復号化
    使用場所：models.py(カスタムユーザーのSaveメソッド)
    """
    signer = Signer() # keyはデフォルトの「SECRET_KEY」を使用
    # ＤB内で辞書を暗号化した要素を復号
    original = signer.unsign_object(target)
    # 辞書内のキーとバリューを取り出す
    value_list =  [k+':'+v for k, v in original.items()]
    # リスト内には１つしか要素がないので０番目の要素を取り出す
    value = value_list[0]
    # 最後にテキストをsignした暗号物を復号する
    plain_text = signer.unsign(value)
    return plain_text

