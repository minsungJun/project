
chatSocket.onopen = () => { //웹 소켓 생성 완료시 실행
    chatSocket.send(JSON.stringify({
        'send_type': 'enter',
        'user_name': userName,
        'room_name': roomName,
    }));
};

chatSocket.onclose = () => { //웹 소켓 종료시에 실행
    chatSocket.send(JSON.stringify({
        'send_type': 'close',
        'user_name': userName,
        'room_name': roomName,
    }));
};

function disconnect(){
    chatSocket.onclose();
}

window.onbeforeunload = function() {
    console.log("[window onbeforeunload] : [start]");
    console.log("");
    disconnect();
    
    //return "브라우저를 종료하시겠습니까?";
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
        dice_clear();
        for(let i=0; i<15; i++){
            document.getElementById('p'+String(user_number)+String(i)).textContent = dice_value[i];
        }
    }

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

