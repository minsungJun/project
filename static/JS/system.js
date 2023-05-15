
chatSocket.onopen = () => { //웹 소켓 생성 완료시 실
    chatSocket.send(JSON.stringify({
        'send_type': 'enter',
        'user_name': userName,
        'room_name': roomName,
    }));
};

chatSocket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    console.log(data);

    let today = new Date();
    let hours = today.getHours(); // 시
    let minutes = today.getMinutes();  // 분
    let seconds = today.getSeconds();  // 초
    let presentTime = (hours + ':' + minutes + ':' + seconds);


    //메세지 수신
    if(data['send_type'] == 'message'){
        let message = data['message'];
        //document.write('#chat-log').value;
        //#실패 로그를 남길때 각자 자기 이름을 남김(남이 보낸 문자에 자기 이름 남김), 통신이 되기는 함
        //document.querySelector("#chat-log").value += (userName + '\n');
        //성공함 왜?, 왜 됐는지는 모르겠음;;, chatSocket.onmessage이 웹소캣에 메시지가 들어왔을때
        //이벤트 발생이기때문에 메시지가 들어왔을때의 데이터(밑의 형식의 데이터)를 이용해야 하는듯?
        document.querySelector("#chat-log").value += (data['user_name'] + '\n'); //유저 출력 성고
        document.querySelector("#chat-log").value += (message + '\t'); //메시지 내용 출력 성공
        //document.querySelector("#chat-log").value += (presentTime + '\n'); //굳이 쓸필요 없음?
        document.querySelector("#chat-log").value += (presentTime + '\n');// 현재 시간 출력
    }


    //주사위 값 수신
    else if(data['send_type'] == 'dice_roll'){
        let dice_value = data['type'];
        let roll_cnt = data['roll_cnt'];
        let user_number = data['user_number'];
        let used_score = data['used_score'];
        //console.log(used_score);
        for(let i=0; i<5; i++){
            document.getElementById('d'+String(i)).textContent = dice_value[i];
        }
        preview_score(dice_value, user_number, used_score);
        document.getElementById('test-submit').textContent = 'Re Roll (' + roll_cnt + '/ 3)';
    }

    //점수 수신
    else if(data['send_type'] == 'score_table'){
        let dice_value = data['type'];
        let user_number = data['user_number'];
        let game_over = data['game_over'];
        let user_score = data['user_score'];
        dice_clear();
        //게임 오버
        if(game_over==true){
            console.log("gameover test333");
            let is_win = check_winner(user_score, userName)
            document.querySelector("#chat-log").value += ("!!GAME OVER!!");
            if(is_win == 0){
                alert("WINNER");
            }
            else if(is_win == 1){
                alert("LOSER");
            }
            else if(is_win == 2){
                alert("DRAW")
            }
            document.getElementById("is_win_input").value = is_win;
            document.getElementById("score_input").value = user_score[userName];
            document.getElementById("decide_winner").submit();
        }
        for(let i=0; i<15; i++){
            document.getElementById('p'+String(user_number)+String(i)).textContent = dice_value[i];
        }
        
    }

};

function check_winner(dic, name){
    let score_list = Object.keys(dic);
    let myscore = dic[name];
    let otherscore;

    score_list.indexOf(name) == 0 ? otherscore = dic[score_list[1]] : otherscore = dic[score_list[0]];

    if(myscore > otherscore){//승
        return 0; 
    }
    else if(myscore < otherscore){//패
        return 1;
    }
    else if(myscore == otherscore){//무
        return 2;
    }

}


chatSocket.onclose = (e) => {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").addEventListener("keyup",(e) => {
    if (e.keyCode === 13) {
        document.querySelector("#chat-message-submit").click();
    }
});

document.querySelector("#chat-message-submit").addEventListener("click", (e) => {
    let messageInputDom = document.querySelector("#chat-message-input");
    let message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'send_type': 'message',
        'user_name': userName,
        'message' : message,
        //'present_time': presentTime
    }));

    messageInputDom.value = '';
});

