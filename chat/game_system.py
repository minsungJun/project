import copy
from random import *


class System:
    def __init__(self):
        self.dice = [-1, -1, -1, -1, -1]
        self.dice_lock = [False, False, False, False, False]
        self.score_table = [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0]
        self.used_score = [False, False, False, False, False,  False, True, False, False, False,  False, False, False, False, True]
        self.roll_cnt = 0
        self.yachu_cnt = 0

    def end_turn(self):
        self.roll_cnt = 0
        self.sum_scores()

    def check_overlap_yachu(self):
        if self.yachu_cnt > 0:
            if self.dice.count(self.dice[0]) == 5:
                self.score_table[12] += 50

    '''
    def yachu(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        if temp.count(temp[0]) == 5:
            total = 50
            self.yachu_cnt += 1
        self.score_table[12] += total
        self.end_turn()
    '''

    def roll(self):
        if self.roll_cnt < 100:
            for i in range(5):
                if not self.dice_lock[i]:
                    self.dice[i] = randint(1, 6)
            self.roll_cnt += 1

    def number(self, num):
        total = 0
        for i in range(5):
            if self.dice[i] == num:
                total += num
        self.score_table[num - 1] = total
        self.used_score[num - 1] = True
        self.homework()
        self.check_overlap_yachu()
        self.end_turn()

    def homework(self):
        if self.score_table[0] + self.score_table[1] + self.score_table[2] + self.score_table[3] + self.score_table[4] + \
                self.score_table[5] >= 63:
            self.score_table[6] = 35

    # 안넣은 기능 : 리롤 횟수 제한, 턴 체크, 턴 넘기기, 야추 중복 판별, 점수 중복 입력 방지, 점수 미리 보기
    # 구현한 기능 : 리롤 횟수 제한, 턴 체크, 턴 넘기기,
    # 턴 넘기기 기능 구현할 때, 입력값 넣어서 점수 미리 보기 인지 아닌지 확인 하는거 해야됨

    def triple(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        temp.sort()
        if temp[0] == temp[2] or temp[1] == temp[3] or temp[2] == temp[4]:
            total = sum(self.dice)
        self.score_table[7] = total
        self.used_score[7] = True
        self.check_overlap_yachu()
        self.end_turn()

    def fourcard(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        temp.sort()
        if temp[0] == temp[3] or temp[1] == temp[4]:
            total = sum(self.dice)
        self.score_table[8] = total
        self.used_score[8] = True
        self.check_overlap_yachu()
        self.end_turn()

    def fullhouse(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        temp.sort()
        if ((temp[0] == temp[2]) and (temp[3] == temp[4])) or ((temp[2] == temp[4]) and (temp[0] == temp[1])):
            total = sum(self.dice)
        self.score_table[9] = total
        self.used_score[9] = True
        self.check_overlap_yachu()
        self.end_turn()

    def Sstraight(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        if (1 in temp and 2 in temp and 3 in temp and 4 in temp) or (
                5 in temp and 2 in temp and 3 in temp and 4 in temp) or (
                5 in temp and 6 in temp and 3 in temp and 4 in temp):
            total = 15
        self.score_table[10] = total
        self.used_score[10] = True
        self.check_overlap_yachu()
        self.end_turn()

    def Lstraight(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        if (1 in temp and 2 in temp and 3 in temp and 4 in temp and 5 in temp) or (
                2 in temp and 3 in temp and 4 in temp and 5 in temp and 6 in temp):
            total = 30
        self.score_table[11] = total
        self.used_score[11] = True
        self.check_overlap_yachu()
        self.end_turn()

    def yachu(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        if temp.count(temp[0]) == 5:
            total = 50
            self.yachu_cnt += 1
        self.score_table[12] += total
        self.used_score[12] = True
        self.end_turn()

    def choice(self):
        total = 0
        temp = copy.deepcopy(self.dice)
        for i in range(5):
            total += temp[i]
        self.score_table[13] = total
        self.used_score[13] = True
        self.check_overlap_yachu()
        self.end_turn()

    def sum_scores(self):
        total = 0
        for i in range(len(self.score_table) - 1):
            total += self.score_table[i]
        self.score_table[14] = total
