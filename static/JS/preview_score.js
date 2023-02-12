//받아올 값 : 주사위 값, 유저 번호, 기능이름? 몇번째 기능인지? 이건 하드코딩해도 되려나
  //JS에서 먼저 주사위 값을 계산해서 띄워놓을 예정
  //주사위 값을 받아오고 그 주사위 값으로 JS에서 계산을 먼저 할거임
  //유저 번호를 받아내서 왼쪽, 오른쪽 구분해서 띄워놓기
  //
  

  function preview_num(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
      let total = 0;
      for(var i=0; i<5; i++){
        if(dice_value[i] == func_num + 1) total += dice_value[i];
      }
      document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')';
    }
  }

  function preview_homework(dice_value, user_number, func_num){
    let total = 0;
    //이건 1~6값 총 합을 보여주는게 베스트인데 이러면 주사위값 수신과 점수판 수신을 합치는게 나을지도 모르겠음 근데 dice_clear가 걸리네 고민이 더 필요함
    document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')';
  }

  function preview_triple(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
      let total = 0;
      var temp = [...dice_value];
      temp.sort((a,b) => a-b);
      for(var i=1; i<4; i++){
        if(temp[i]===temp[i-1] && temp[i]===temp[i+1]){
          total = temp.reduce((a, b) => (a + b));//배열의 합계 리턴
          break;
        }
      }
      document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')'
    }
  }

  function preview_fourcards(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
        let total = 0;
        var temp = [...dice_value];
        temp.sort((a,b) => a-b);
        
        if(temp[0]===temp[3] || temp[1]===temp[4]){
            total = temp.reduce((a, b) => (a + b));//배열의 합계 리턴
        }
        document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')'
    }
  }

  function preview_fullhouse(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
        var total = 0;
        var temp = [...dice_value];
        temp.sort((a,b) => a-b);

        if( ( (temp[0]===temp[1]&&temp[1]===temp[2]) && (temp[3]===temp[4]) ) || ( (temp[2]===temp[3]&&temp[3]===temp[4]) && (temp[0]===temp[1]) ) ) {
            total = temp.reduce((a, b) => (a + b));//배열의 합계 리턴
          }
        document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')'
    }
  }

  function preview_Sstraight(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
        var total = 0;
        if( (dice_value.includes(1)&&dice_value.includes(2)&&dice_value.includes(3)&&dice_value.includes(4)) ||
        (dice_value.includes(5)&&dice_value.includes(2)&&dice_value.includes(3)&&dice_value.includes(4)) ||
      (dice_value.includes(5)&&dice_value.includes(6)&&dice_value.includes(3)&&dice_value.includes(4)) ){
        total = 15;
      }
    }
    document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')'
  }

  function preview_Lstraight(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
        var total = 0;
        if( (dice_value.includes(1)&&dice_value.includes(2)&&dice_value.includes(3)&&dice_value.includes(4)&&dice_value.includes(5)) ||
      (dice_value.includes(5)&&dice_value.includes(2)&&dice_value.includes(3)&&dice_value.includes(4)&&dice_value.includes(6))  ) {
            total = 30;
        }
        document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')'
    }
  }

  function preview_yachu(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
        var total = 0;
        for(var i=0; i<5; i++){
            if(dice_value[i] != dice_value[0])break;
            if(i==4){
              total = 50;
            }  
        }
        document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')'
    }
  }

  function preview_choice(dice_value, user_number, used_score, func_num){
    if(used_score[func_num]==false){
        var temp = [...dice_value];
        var total = temp.reduce((a, b) => (a + b));//배열의 합계 리턴
        document.getElementById('p'+String(user_number)+String(func_num)).textContent = '(+' + total + ')'
    }
  }


  function preview_score(dice_value, user_number, used_score){
    for(var i=0; i<6; i++){
        preview_num(dice_value, user_number, used_score, i);
    }
  //function preview_homework();
    preview_triple(dice_value, user_number, used_score, 7);
    preview_fourcards(dice_value, user_number, used_score, 8);
    preview_fullhouse(dice_value, user_number, used_score, 9);
    preview_Sstraight(dice_value, user_number, used_score, 10);
    preview_Lstraight(dice_value, user_number, used_score, 11);
    preview_yachu(dice_value, user_number, used_score, 12);
    preview_choice(dice_value, user_number, used_score, 13);
  }

  function color(i){
    lock[i] = !lock[i];
    if(lock[i] == true)document.getElementById('d'+String(i)).style.background = 'rgb(255,100,100)';
    if(lock[i] == false)document.getElementById('d'+String(i)).style.background = 'rgb(255,255,255)';
  }