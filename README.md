# DjangoフレームワークによるWeb日報登録システム（未完成）

## 概要

YouTubeで発信されている徳田啓（トクタ　ケイ）さんによる「Web日報登録システム」の開発をPythonのDjangoフレームワークで開発してみました。

↓↓↓
- [【開発実況シリーズ】店舗用Web予約システムを作る#1 企画編【プログラミング】](https://www.youtube.com/watch?v=6nM48VIWr4I&list=PLgx8xyH2m7OUtmSNw_RLOUDiBnZjhz0d8)

上記動画では以下のようなプログラムによって「企画」～「テスト＆仮運用」までの工程を解説しながら開発を行ってくれています。

|ツール|ツール名|
|----|----|
|IDE|VSCode|
|データベース|MySQL|
|プログラミング言語|PHP|
|フロント（UI）|BootStrap|

私はPython使いであるためアイディア等を参考にさせて頂き、プログラミング言語のPHPの部分を**PythonのDjangoフレームワーク**に置き換えて開発を行ってみました。

## 各アクセス先のご紹介

ご紹介といっても、YouTubeで発信されている徳田啓さんが作成したUIをそのまま真似しているのでご了承ください。

機能に関しては泥臭さもありますが試行錯誤しながら実装しました。

### 社員用ログイン画面

![work_login](https://user-images.githubusercontent.com/51676019/200212822-0def97c7-e374-4f9c-9a7c-8dfe74b26d07.jpg)


### 社員用月別リスト画面



### 管理者用ログイン画面



### 管理者用社員一覧画面



### 管理者用月別リスト画面


...

追加機能として、「月別リスト」の表示でタイムスタンプが押されていない日付もデータベースに保存しておく（日付は保存する
月が切り替わるタイミングで一月分のデータを予め一括保存しておき、社員が勤怠保存する際のデータは更新として保存する
なのでモーダルでは更新するための実装とする
