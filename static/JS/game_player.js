document.querySelector("#test-submit").addEventListener("click", (e) => {
  chatSocket.send(JSON.stringify({
      'send_type' : 'dice_roll',
      'lock_data' : lock,
      'user_name' : userName,
      'room_name' : roomName,
  }));
});

  function dice_clear(){
    lock = [false, false, false, false, false];
    for(let i=0; i<5; i++){
        document.getElementById('d'+String(i)).innerHTML = 'D'+String(i+1);
        document.getElementById('d'+String(i)).style.background = 'rgb(255,255,255)';
    }
    document.getElementById('test-submit').innerHTML = 'START';
  }

  function number(num){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_number',
        'dice_num'  : num,
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function triple(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_triple',
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function fourcard(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_fourcard',
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function fullhouse(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_fullhouse',
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function Sstraight(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_Sstraight',
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function Lstraight(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_Lstraight',
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function yachu(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_yachu',
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function choice(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_choice',
        'user_name' : userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }
  //받아올 값 : 주사위 값, 유저 번호, 기능이름? 몇번째 기능인지? 이건 하드코딩해도 되려나
  //JS에서 먼저 주사위 값을 계산해서 띄워놓을 예정
  //주사위 값을 받아오고 그 주사위 값으로 JS에서 계산을 먼저 할거임
  //유저 번호를 받아내서 왼쪽, 오른쪽 구분해서 띄워놓기
  //
  

  function preview_num(dice_value, user_number, func_num){
    let total = 0;
    for(var i=0; i<5; i++){
      if(dice_value[i] == func_num + 1) total += dice_value[i];
    }
    document.getElementById('p'+String(user_number)+String(func_num)).innerHTML = '(+' + total + ')';
  }

  function preview_score(dice_value, user_number){
    aaa(dice_value, user_number, 0);
    aaa(dice_value, user_number, 1);
    aaa(dice_value, user_number, 2);
    aaa(dice_value, user_number, 3);
    aaa(dice_value, user_number, 4);
    aaa(dice_value, user_number, 5);
  }



  function color(i){
      lock[i] = !lock[i];
      if(lock[i] == true)document.getElementById('d'+String(i)).style.background = 'rgb(255,100,100)';
      if(lock[i] == false)document.getElementById('d'+String(i)).style.background = 'rgb(255,255,255)';
  }