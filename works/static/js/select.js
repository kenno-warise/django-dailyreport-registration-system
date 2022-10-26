
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
// セレクトメニューの値が変更された時に実行される処理
dateValue.addEventListener('change', (event) => {
  // セレクトメニュー内で選択された値の順番を取得する
  const dateValueId = dateValue.selectedIndex;
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
    let query_list = json.query_list;
    let edit_icon = '<i class="fa-solid fa-pencil" id="pencil-icon"></i>'
    let table_body = document.getElementById('table-body');
    table_body.innerHTML = '';
    {{ query_list }}
    for (let query of query_list) {
      let tr_block = document.createElement('tr');
      let td_block_1 = document.createElement('td');
      let td_block_2 = document.createElement('td');
      let td_block_3 = document.createElement('td');
      let td_block_4 = document.createElement('td');
      let td_block_5 = document.createElement('td');
      let td_block_6 = document.createElement('td');
      td_block_1.innerHTML = `${ query.date }`;
      td_block_2.innerHTML = `${query.start_time}`;
      td_block_3.innerHTML = `${query.end_time}`;
      td_block_4.innerHTML = `${query.break_time}`;
      td_block_5.innerHTML = `${query.comment}`;
      td_block_6.innerHTML = `${edit_icon}`;
      tr_block.appendChild(td_block_1);
      tr_block.appendChild(td_block_2);
      tr_block.appendChild(td_block_3);
      tr_block.appendChild(td_block_4);
      tr_block.appendChild(td_block_5);
      tr_block.appendChild(td_block_6);
      table_body.appendChild(tr_block);
    }
  }
  // 定義した関数を実行する
  menu_list();
});
