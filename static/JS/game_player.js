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
      document.getElementById('d'+String(i)).style.background = 'rgb(255,255,255)';
  }
  document.getElementById('test-submit').textContent = 'START';
}

function number(num){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_number',
      'dice_num' : num,
      'user_name': userName,
      'room_name' : roomName,
  }));
}

function triple(){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_triple',
      'user_name': userName,
      'room_name' : roomName,
  }));
}

function fourcard(){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_fourcard',
      'user_name': userName,
      'room_name' : roomName,
  }));
}

function fullhouse(){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_fullhouse',
      'user_name': userName,
      'room_name' : roomName,
  }));
}

function Sstraight(){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_Sstraight',
      'user_name': userName,
      'room_name' : roomName,
  }));
}

function Lstraight(){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_Lstraight',
      'user_name': userName,
      'room_name' : roomName,
  }));
}

function yachu(){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_yachu',
      'user_name': userName,
      'room_name' : roomName,
  }));
}

function choice(){
  chatSocket.send(JSON.stringify({
      'send_type' : 'game_choice',
      'user_name': userName,
      'room_name' : roomName,
  }));
}


