$(function() {
  /* 定数 */
  const PAGES = {
    'page-top': '画像を選択してください。',
    'page-ready': 'この画像を解析します。',
    'page-detecting': '解析中…',
    'page-result': '解析結果です。',
    'page-fail': 'エラーが発生しました。'
  };
  const  TARGETS = {
    0: {
      'name': '解析結果０',
      'color': 'black'
    },
    1: {
      'name': '解析結果１',
      'color': 'rgb(255, 177, 89)'
    },
    2: {
      'name': '解析結果２',
      'color': 'rgb(255, 68, 75)'
    },
    3: {
      'name': '解析結果３',
      'color': 'rgb(107, 121, 255)'
    },
    4: {
      'name': '解析結果４',
      'color': 'rgb(255, 147, 155)'
    }
  };
  const BG_COLOR ='white';
  const TEXT_COLOR = 'rgb(74, 52, 44)';
  const CS_FONT_SIZE = 30;

  /* グローバル変数 */
  var now = 'page-top';
  var isUpload = false;

  /* onのイベントセット */

  // リセット
  $('.reset-all').on('click', function () {
    resetAll();
  });
  // ファイルアップロード時
  $('#sendFile').on('change', function (evt) {
    handleFileSelect(evt);
  });
  // 画像投稿
  $('#imgForm').on('submit', function(e) {
    e.preventDefault();
    var formData = new FormData($(this).get(0));
    $.ajax($(this).attr('action'), {
      type: 'post',
      timeout: 60000,
      processData: false,
      contentType: false,
      data: formData,
      success: movePage('page-detecting')
    }).done(function(response){
      drawResult(response['result']);
      movePage('page-result')
    }).fail(function() {
      failDetecting();
    });
    return false;
  });

  /* ページ遷移 */

  // 次のページに遷移
  function movePage(targetPage) {
    // 現在のページの要素を非表示
    changeAllDisplayState(now, 'none');
    // 現在のページを次のページに変更
    now = targetPage;
    // 次のページの要素を表示
    changeAllDisplayState(now, 'block');
    // メッセージをセットする
    setMessage(PAGES[now]);
  }

  // 同一クラスの表示変更
  function changeAllDisplayState(className, displayState) {
    $('.' + className).css('display', displayState);
  }

  // ボスのメッセージを書き換え
  function setMessage(msg) {
    $('#msg').html(msg);
  }

  // エラーをページに遷移
  function failDetecting() {
    movePage('page-fail');
  }

  // 全部リセット
  function resetAll() {
    // ファイルをリセット
    $('#sendFile').val('');
    // canvasの中の画像を削除
    var canvas = $('#cnvs');
    var ctx = canvas[0].getContext('2d');
    ctx.clearRect(0, 0, canvas.width(), canvas.height());
    // アップロード状態をリセット
    isUpload = false;
    displayCanvasImg(isUpload);
    // topへ遷移
    movePage('page-top');
  }

  /* アップロードファイル周り */

  // アップロードした画像をcanvasで描画
  function loadImageFile(uploadFile) {
    var canvas = $('#cnvs');
    var ctx = canvas[0].getContext('2d');
    var image = new Image();
    var fr = new FileReader();
    // ファイルをロードしたらコールバック
    fr.onload = function(evt) {
      // 画像をロードしたらコールバック
      image.onload = function() {
        var cnvsW = image.width;
        var cnvsH = cnvsW*image.naturalHeight/image.naturalWidth;
        canvas.attr('width', cnvsW);
        canvas.attr('height', cnvsH);
        ctx.drawImage(image, 0, 0, cnvsW, cnvsH);
        // 画像の表示
        isUpload = true;
        displayCanvasImg(isUpload);
      }
      image.src = evt.target.result;
    }
    fr.readAsDataURL(uploadFile);
  }

  // 画像のロード状況から表示・非表示を切り替える
  function displayCanvasImg(displayFlag) {
    if (displayFlag) {
      $('#display-img').show();
    } else {
      $('#display-img').hide();
    }
  }

  // 解析結果の描画
  function drawResult(result) {
    var canvas = $('#cnvs');
    var ctx = canvas[0].getContext('2d');
    ctx.beginPath();
    for (var i = 0; i <= result.length - 1; i ++) {
      var label = result[i]['analysis']['label'];
      drawRect(ctx, result[i]['rect'], label);
      drawNameRect(ctx, result[i]['rect'], label);
      drawName(ctx, result[i]['rect'], label, result[i]['analysis']['rate']);
    }
  }

  // 四角枠を描画する
  function drawRect(ctx, rect, label) {
    ctx.lineWidth = 5;
    ctx.strokeStyle = TARGETS[label]['color'];
    ctx.strokeRect(rect['left'], rect['top'], rect['right'] - rect['left'], rect['bottom'] - rect['top']);
  }

  // 名前枠を描画する
  function drawNameRect(ctx, rect, label) {
    // 枠の幅を求める
    var rectWidth = TARGETS[label]['name'].length * CS_FONT_SIZE + 15
    // 背景
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(rect['left'], rect['bottom'], rectWidth, CS_FONT_SIZE * 2 + 15);
    // 枠
    ctx.lineWidth = 5;
    ctx.strokeStyle = TARGETS[label]['color'];
    var rectWidth = name.length *
    ctx.strokeRect(rect['left'], rect['bottom'], rectWidth, CS_FONT_SIZE * 2 + 15);
  }

  // 名前を描画する
  function drawName(ctx, rect, label, rate) {
    ctx.font = "bold " + CS_FONT_SIZE + "px 'Arial'";
    ctx.fillStyle = TEXT_COLOR;
    ctx.fillText(TARGETS[label]['name'], rect['left'] + 7.5, rect['bottom'] + CS_FONT_SIZE + 5);
    ctx.fillText(rate + '%', rect['left'] + 7.5, rect['bottom'] + CS_FONT_SIZE * 2 + 7.5);
  }

  // アップロードした画像から情報取得
  function handleFileSelect(evt) {
    var files = evt.target.files;
    if (!files.length) {
      failDetecting();
      return;
    }
    loadImageFile(files[0]);
    movePage('page-ready');
  }
});
