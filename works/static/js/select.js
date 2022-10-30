
// ①Django側にPOST送信する際に記述する"お決まりのコード"
const getCookie = (name) => {
  if (document.cookie && document.cookie !== '') {
    for (const cookie of document.cookie.split(';')) {
      const [key, value] = cookie.trim().split('=');
      if (key === name) {
	return decodeURIComponent(value);
      }
    }
  }
};
const csrftoken = getCookie('csrftoken');

// ②選択されたセレクトメニュー情報をDjango側にPOST送信してデータを取得する
// セレクトメニュー内の要素を取得する
const dateValue = document.getElementById('date_pulldown');
const adminValue = document.getElementById('admin');
// セレクトメニューの値が変更された時に実行される処理
dateValue.addEventListener('change', (event) => {
  // セレクトメニュー内で選択された値の順番を取得する
  const dateValueId = dateValue.selectedIndex;
  const adminBool = adminValue.textContent;
  // セレクトメニュー内で選択された値のidを取得する
  const selectedDate = dateValue[dateValueId].value;
  // セレクトメニュー内の要素を取得する
  // 非同期処理を記述する
  async function menu_list() {
    const url = '/pulldown-access/';
    let res = await fetch(url, {
      method: 'POST',
      headers: {
	'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
	'X-CSRFToken': csrftoken,
      },
      // str型で取得してしまう
      body: `month_val=${selectedDate}`
    });
    let json = await res.json();
    // pulldown-accessからWorkインスタンスを取得
    let query_list = json.query_list;
    // 既存の<table>を取得
    let table_body = document.getElementById('table-body');
    // <table>内の要素を空にする
    table_body.innerHTML = '';
    // 本日以外の編集ボタンを非表示にするための日付要素
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth() + 1;
    const day = now.getDate();
    // console.log(year+'-'+month+'-'+day)
    for (let query of query_list) {
      // <tr>を作成
      let tr_block = document.createElement('tr');
      // <th>を作成
      let td_block_1 = document.createElement('th');
      // <td>を作成
      let td_block_2 = document.createElement('td');
      let td_block_3 = document.createElement('td');
      let td_block_4 = document.createElement('td');
      let td_block_5 = document.createElement('td');
      let td_block_6 = document.createElement('td');
      let td_block_7 = document.createElement('td');
      let td_block_8 = document.createElement('td');
      let td_block_9 = document.createElement('td');
      // <th>内に日付要素を代入
      td_block_1.innerHTML = `${ query.week }`;
      // <td>内に出勤時間を代入
      td_block_2.innerHTML = `${query.start_time}`;
      td_block_3.innerHTML = `${query.end_time}`;
      td_block_4.innerHTML = `${query.break_time}`;
      td_block_5.innerHTML = `${query.comment}`;
      // プルダウンが押された際に、query.dateが本日の日付と同じでない場合は空の要素を挿入し編集できないようにする
      // もしくは管理者（True）だった場合は編集ボタン表示
      if (query.date == year+'-'+month+'-'+day || adminBool == 'True') {
      td_block_6.innerHTML = `<button type="button" class="btn btn-default h-auto py-0" data-bs-toggle="modal" data-bs-target="#exampleModal" data-day=${query.date}><i class="fa-solid fa-pencil" id="pencil-icon"></i></button>`;
      } else {
	td_block_6.innerHTML = ``;
      }
      // ユーザーID用の<td>にhidden属性を追加
      td_block_7.setAttribute('hidden', '');
      td_block_7.innerHTML = `${query.user_id_id}`;
      // 日付用の<td>にhidden属性を追加
      td_block_8.setAttribute('hidden', '');
      td_block_8.innerHTML = `${query.date}`;
      // WorkモデルID用の<td>にhidden属性を追加
      td_block_9.setAttribute('hidden', '');
      td_block_9.innerHTML = `${query.id}`;
      // <tr>に各テーブルブロックを追加
      tr_block.appendChild(td_block_1);
      tr_block.appendChild(td_block_2);
      tr_block.appendChild(td_block_3);
      tr_block.appendChild(td_block_4);
      tr_block.appendChild(td_block_5);
      tr_block.appendChild(td_block_6);
      tr_block.appendChild(td_block_7);
      tr_block.appendChild(td_block_8);
      tr_block.appendChild(td_block_9);
      // <table>に<tr>を追加
      table_body.appendChild(tr_block);
    }
  }
  // 定義した関数を実行する
  menu_list();
});

