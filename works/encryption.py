from django.core.signing import Signer


def encryption(target):
    """暗号化"""
    signer = Signer() # keyはデフォルトの「SECRET_KEY」を使用
    value = signer.sign(target)
    value_list = [value.split(':')]
    dict_sign = dict(value_list)
    signed_obj = signer.sign_object(dict_sign)
    return signed_obj


def decryption(target):
    """復号化"""
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

