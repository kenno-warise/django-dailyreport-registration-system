#!/bin/bash
# コードチェックとテストを実行するためのシェルスクリプト
# 作成日 2022-11-04

echo 'blackチェック'
# pep8に準拠した妥協のないコードフォーマッター
black works/views.py works/urls.py works/forms.py works/models.py works/admin.py config/urls.py config/settings.py
echo ''
echo 'flake8チェック'
# pep8に準拠していないコードを取得する
flake8 works/views.py works/urls.py works/forms.py works/models.py works/admin.py config/urls.py config/settings.py
echo ''
echo 'isortチェック'
# pep8に準拠したimport文を綺麗にコーディングし直す
isort works config/urls.py
echo ''
echo 'DjangoテストとCoverageの実行'
# DjangoのUnitTest
coverage run --include=works/* --omit=works/migrations/* manage.py test works
echo ''
echo 'Coverageの詳細表示'
# Coverageレポートの出力
coverage report
# カバレッジの進捗をHTMLで表示
coverage html
echo ''
echo 'Coverageのリンク'
# カバレッジHTMLのリンク↓↓
echo file:///C:/Users/warik/Documents/PYTHON/django-app/django-works/htmlcov/index.html
