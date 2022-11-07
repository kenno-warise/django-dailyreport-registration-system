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

### 社員用のログイン画面（login）

社員専用のログイン画面です。

ログアウト、もしくは月別リスト画面へアクセスしようとするとこの画面へリダイレクトされます。

![work_login](https://user-images.githubusercontent.com/51676019/200212822-0def97c7-e374-4f9c-9a7c-8dfe74b26d07.jpg)

認証に失敗するとエラーとなりもう一度やり直しになります。

![work_login_error](https://user-images.githubusercontent.com/51676019/200213810-01b8b79b-ff9c-45f0-8e45-b41fe66ef0df.jpg)

### 社員用の月別リスト画面（index）

社員用の月別リスト画面です。

「出勤時間」と「退勤時間」が登録されていない場合は、アクセスされるたびに自動で以下のようなモーダルが自動実行されます。

![work_index_modal](https://user-images.githubusercontent.com/51676019/200213853-8c36d5c1-5db7-453f-9748-a7c4e8574667.jpg)

下線の打刻ボタンを押すことで、現在の時刻が入力されます。

![work_index_modal_2](https://user-images.githubusercontent.com/51676019/200213884-d69dc0d4-079c-4bb6-8b4f-9dd12ae0f05d.jpg)

時間のフォーマット以外の文字列が入力され、登録ボタンが押されるとエラーとなります。

![work_index_modal_error](https://user-images.githubusercontent.com/51676019/200213915-3b924d3c-f3c4-4a1b-affd-733c185b2f32.jpg)

「出勤時間」共に「退勤時間」が登録されていると、月別リストが表示されます。

左上のプルダウンは今月を含めた過去12ヵ月分の月を表示することができます。

![work_index_list](https://user-images.githubusercontent.com/51676019/200213928-30e1aaad-a5e6-4aff-9d84-757b0837a109.jpg)


### 管理者用ログイン画面

管理者専用のログイン画面となります。

![work_admin_login](https://user-images.githubusercontent.com/51676019/200214923-901d022a-3f0a-41aa-8ad6-98d56cd5f139.jpg)

管理者以外のユーザーがログインを試みるとエラーとなります。

![work_admin_login_error](https://user-images.githubusercontent.com/51676019/200214944-aa552932-2e15-4549-9dca-959ce46b4a92.jpg)

### 管理者用社員一覧画面

データベースに保存されている社員の一覧画面です。

管理者は各社員の日報情報を表示することができます。

![work_admin_userlist](https://user-images.githubusercontent.com/51676019/200215015-df3d6b2c-87b2-4289-8324-2897432cea62.jpg)

### 管理者用月別リスト画面

管理者用の月別リスト画面です。

編集を自由に行うことができます。

![work_admin_userresult](https://user-images.githubusercontent.com/51676019/200215072-b85b7bae-726b-4070-876f-c102bec4b6ca.jpg)

編集ボタンを押すとモーダルが実行されます。

![work_admin_userresult_modal](https://user-images.githubusercontent.com/51676019/200215087-6f5d2501-ed6e-4a61-b712-63e6e117a50f.jpg)

上記以外の社員の日報情報です。
![work_admin_userresult_2](https://user-images.githubusercontent.com/51676019/200215101-25d81a66-909b-455d-89a2-e55b0dca5d21.jpg)
