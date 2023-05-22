var rollBtn = document.querySelector('.rollBtn');

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

var Dicetest = function(test){
    this.cubetest = document.querySelector(test);
    this.currentClasstest = '';

    this.rollDicetest1 = function(dice_num) {
        var randNumtest = getRandomInt(1,7);
        var showClasstest = 'show-' + randNumtest;
         
        console.log(showClasstest)
        console.log(this.cubetest)
         
        if ( this.currentClasstest ) {
          console.log(this.currentClasstest)
          this.cubetest.classList.remove( this.currentClasstest );
        }
        this.cubetest.classList.add( showClasstest );
        this.currentClasstest = showClasstest;

        return
       }

    this.rollDicetest = function(dice_num) {
      var randNumtest = dice_num;
      var showClasstest = 'show-' + randNumtest;
        
      console.log(showClasstest)
      console.log(this.cubetest)
        
      if ( this.currentClasstest ) {
        console.log(this.currentClasstest)
        this.cubetest.classList.remove( this.currentClasstest );
      }
      this.cubetest.classList.add( showClasstest );
      this.currentClasstest = showClasstest;

      return
    }
}


let test1 = new Dicetest('.cube1');
let test2 = new Dicetest('.cube2');
let test3 = new Dicetest('.cube3');
let test4 = new Dicetest('.cube4');
let test5 = new Dicetest('.cube5');

function dice_roll(dice_arr){
  console.log('HI!')
  test1.rollDicetest(dice_arr[0]);
  test2.rollDicetest(dice_arr[1]);
  test3.rollDicetest(dice_arr[2]);
  test4.rollDicetest(dice_arr[3]);
  test5.rollDicetest(dice_arr[4]);
}

function dice_roll_test(){
  testarr = [1,2,3,4,5]
  test1.rollDicetest1(testarr[0]);
  test2.rollDicetest1(testarr[1]);
  test3.rollDicetest1(testarr[2]);
  test4.rollDicetest1(testarr[3]);
  test5.rollDicetest1(testarr[4]);
}

function dice_roll_test2(testarr){
  test1.rollDicetest(testarr[0]);
  test2.rollDicetest(testarr[1]);
  test3.rollDicetest(testarr[2]);
  test4.rollDicetest(testarr[3]);
  test5.rollDicetest(testarr[4]);
}

  rollBtn.addEventListener("click", test1.rollDicetest1.bind(test1));
  rollBtn.addEventListener("click", test2.rollDicetest1.bind(test2));
  rollBtn.addEventListener("click", test3.rollDicetest1.bind(test3));
  rollBtn.addEventListener("click", test4.rollDicetest1.bind(test4));
  rollBtn.addEventListener("click", test5.rollDicetest1.bind(test5));
//rollBtn1.onclick = rollDice(cube1)