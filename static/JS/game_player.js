document.querySelector("#test-submit").addEventListener("click", (e) => {
  chatSocket.send(JSON.stringify({
      'send_type' : 'dice_roll',
      'lock_data' : lock,
      'user_name': userName,
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
        'dice_num' : num,
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function triple(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_triple',
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function fourcard(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_fourcard',
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function fullhouse(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_fullhouse',
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function Sstraight(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_Sstraight',
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function Lstraight(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_Lstraight',
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function yachu(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_yachu',
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }

  function choice(){
    chatSocket.send(JSON.stringify({
        'send_type' : 'game_choice',
        'user_name': userName,
        'room_name' : roomName,
    }));
    dice_clear();
  }


  function color(i){
      lock[i] = !lock[i];
      if(lock[i] == true)document.getElementById('d'+String(i)).style.background = 'rgb(255,100,100)';
      if(lock[i] == false)document.getElementById('d'+String(i)).style.background = 'rgb(255,255,255)';
  }