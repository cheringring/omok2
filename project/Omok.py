import pygame
import time
import sys
import random

# 렌주룰 ( 3 x 3 , 4 x 4 , 장목은 백만 허용 흑은 불가)

pygame.init()

# 이미지 불러오기
mainmenu_background = pygame.image.load("Images/mainmenu/background.png")
mainmenu_start = pygame.image.load("Images/mainmenu/start.png")
mainmenu_explain = pygame.image.load("Images/mainmenu/explain.png")
mainmenu_finish = pygame.image.load("Images/mainmenu/finish.png")
mainmenu_start_click = pygame.image.load("Images/mainmenu/start_click.png")
mainmenu_explain_click = pygame.image.load("Images/mainmenu/explain_click.png")
mainmenu_finish_click = pygame.image.load("Images/mainmenu/finish_click.png")

game_background = pygame.image.load("Images/game/background.png")
game_player_turn = pygame.image.load("Images/game/player_turn.png")
game_player1 = pygame.image.load("Images/game/black.png")
game_player2 = pygame.image.load("Images/game/white.png")

game_finish = pygame.image.load("Images/game/finish.png")
game_finish_draw = pygame.image.load("Images/game/finish_draw.png")
game_pass = pygame.image.load("Images/game/pass.png")

explain_background = pygame.image.load("Images/explain/background.png")
explain_back = pygame.image.load("Images/explain/back.png")
explain_back_click = pygame.image.load("Images/explain/back_click.png")

player_1P = pygame.image.load("Images/player/1P.png")
player_2P = pygame.image.load("Images/player/2P.png")
player_blackPlayer = pygame.image.load("Images/player/blackPlayer.png")
player_whitePlayer = pygame.image.load("Images/player/whitePlayer.png")

# 기본 설정
display_width = 960  # 화면 가로 크기
display_height = 640  # 화면 세로 크기
gameDisplay = pygame.display.set_mode((display_width, display_height))  # 화면 크기설정
pygame.display.set_caption("Omok")  # 타이틀
clock = pygame.time.Clock()
there_is = [[0 for i in range(8)] for j in range(8)]  # 돌이 놓여있는가? 누구의 돌인가? 를 판단
Red = (184, 59, 59)


class Button:  # 버튼
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 클릭여부
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
            gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
            if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                time.sleep(0.2)
                action()
        else:
            gameDisplay.blit(img_in, (x, y))


class Player:  # 플레이어 행동
    def __init__(self, img, turn):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        self.turn = turn

        gameDisplay.blit(game_pass, (810, 580))
        if 930 > mouse[0] > 810 and 640 > mouse[1] > 580 and click[0] and turn == 1:
            self.turn = 2
            time.sleep(0.5)
        elif 930 > mouse[0] > 810 and 640 > mouse[1] > 580 and click[0] and turn == 2:
            self.turn = 1
            time.sleep(0.5)

        for i in range(8):
            for j in range(8):
                if (43 + (i * 70)) < mouse[0] < (113 + (i * 70)) and (40 + (j * 70)) < mouse[1] < (110 + (j * 70)) and \
                        there_is[i][j] == 0:  # 마우스 올려진 좌표 빈칸 검사
                    gameDisplay.blit(img, (53 + (i * 70), 50 + (j * 70)))  # 빈칸일 시 미리보기
                    if click[0] and turn == 1:  # 1P가 빈자리를 클릭
                        if possible_check(i, j, 1):
                            there_is[i][j] = 1
                            self.turn = 2
                    elif click[0] and turn == 2:  # 2P가 빈자리를 클릭
                        if possible_check(i, j, 2):
                            there_is[i][j] = 2
                            self.turn = 1


class CPU:  # 플레이어 행동
    def __init__(self, img, turn):
        self.turn = turn
        able = []
        able_lose=[]
        able_random=[]
        pygame.display.update()

        time.sleep(0.5)


        for i in range(8):
            for j in range(8):
                if there_is[i][j] == 0:
                    able_random.append([i,j])
                    if turn == 1:  # AI가 1P일때
                        if CPU_where_1(i,j,1):
                            able.append([i, j])
                        if CPU_where_2(i,j,2):
                            able_lose.append([i, j])

                    elif turn == 2:  # AI가 2P일때
                        if CPU_where_1(i, j, 2):
                            able.append([i, j])
                        if CPU_where_2(i,j,1):
                            able_lose.append([i, j])
        if len(able)==0 and len(able_lose)==0 and len(able_random)==0:
            if turn == 1:
                self.turn = 2
                time.sleep(0.5)
            elif turn == 2:
                self.turn = 1
                time.sleep(0.5)

        elif len(able) == 0: # 하고자하는 부분이 없으면 (돌이 없으면, 패배할 수 있는 부분이 없으면) 무작위 선택
            index_random = random.randrange(len(able_random))
            i = able_random[index_random][0]
            j = able_random[index_random][1]
            if turn == 1:
                if possible_check(i,j,1):
                    there_is[i][j] = 1
                    self.turn = 2
            elif turn == 2:
                if possible_check(i,j,2):
                    there_is[i][j] = 2
                    self.turn = 1
        else:
            if len(able_lose)==0:
                index = random.randrange(len(able)) # 자신의 돌 주위로 돌을 무작위로 선택
                i = able[index][0]
                j = able[index][1]
                if turn == 1:
                    if possible_check(i, j, 1):
                        there_is[i][j] = 1
                        self.turn = 2
                elif turn == 2:
                    if possible_check(i, j, 2):
                        there_is[i][j] = 2
                        self.turn = 1
            else:
                index = random.randrange(len(able_lose)) # 두지 않으면 지는 부분에 두는 부분 무작위로 선택
                i = able_lose[index][0]
                j = able_lose[index][1]
                if turn == 1:
                    if possible_check(i, j, 1):
                        there_is[i][j] = 1
                        self.turn = 2
                elif turn == 2:
                    if possible_check(i, j, 2):
                        there_is[i][j] = 2
                        self.turn = 1



# CPU 돌이 둬지는 범위

def CPU_where_1(i,j,player):
    check=False

    if there_is[i][j]==0:

        #돌 주변
        
        # 중앙
        if i>0 and j >0 and i<7 and j <7:
            if there_is[i][j-1]==player or there_is[i][j+1]==player or there_is[i-1][j]==player or there_is[i+1][j]==player\
                    or there_is[i-1][j-1]==player or there_is[i+1][j+1]==player or there_is[i+1][j-1]==player or there_is[i-1][j+1]==player:
                check=True
        # 상단
        if i==0 and j >0 and j <7:
            if there_is[i][j-1]==player or there_is[i][j+1]==player or there_is[i+1][j]==player or there_is[i+1][j+1]==player or there_is[i+1][j-1]==player:
                check=True
        #좌상단

        if i==0 and j==0:
            if there_is[i][j+1]==player or there_is[i+1][j]==player or there_is[i+1][j+1]==player:
                check=True

        #우상단

        if i==0 and j==7:
            if there_is[i][j - 1] == player or there_is[i + 1][j] == player or there_is[i + 1][j - 1] == player:
                check = True

        #하단

        if j >0 and i==7 and j <7:
            if there_is[i][j-1]==player or there_is[i][j+1]==player or there_is[i-1][j]==player\
                    or there_is[i-1][j-1]==player or there_is[i-1][j+1]==player:
                check=True

        #좌하단

        if j ==0 and i==7:
            if there_is[i][j+1]==player or there_is[i-1][j]==player or there_is[i-1][j+1]==player:
                check=True

        #우하단

        if i==7 and j ==7:
            if there_is[i][j-1]==player or there_is[i-1][j]==player or there_is[i-1][j-1]==player:
                check=True
        #좌

        if i>0 and j ==0 and i<7:
            if there_is[i][j+1]==player or there_is[i-1][j]==player or there_is[i+1][j]==player or there_is[i+1][j+1]==player or there_is[i-1][j+1]==player:
                check=True
        
        #우

        if i>0 and i<7 and j ==7:
            if there_is[i][j-1]==player or there_is[i-1][j]==player or there_is[i+1][j]==player or there_is[i-1][j-1]==player or there_is[i+1][j-1]==player:
                check=True



    return check

# 상대 승리 막는곳
def CPU_where_2(i,j,oppender):
    


    check_win= False

    if there_is[i][j] == 0:

        there_is[i][j]=oppender

        if winner(there_is):
            check_win=True

        there_is[i][j]=0

    return check_win


# 금수 체크

def possible_check(x,y,player):
    check=True

    if player==2:
        pass
    else: # 흑돌만 제한
        # 3x3

        count_3=0

        #대각선_1

        if (x>0 and x<4) and (y>0 and y<4):
            if there_is[x-1][y-1]==0 and there_is[x+1][y+1]==1 and there_is[x+2][y+2]==1 and there_is[x+3][y+3]==1 and there_is[x+4][y+4]==0:
                count_3+=1
        if (x>1 and x<5) and (y>1 and y<5):
            if there_is[x - 2][y - 2] == 0 and there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1 and \
                    there_is[x + 2][y + 2] == 1 and there_is[x + 3][y + 3] == 0:
                count_3 += 1
        if (x>2 and x<6) and (y>2 and y<6):
            if there_is[x - 3][y - 3] == 0 and there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and \
                    there_is[x + 1][y + 1] == 1 and there_is[x + 2][y + 2] == 0:
                count_3 += 1
        if (x>3 and x<7) and (y>3 and y<7):
            if there_is[x - 4][y - 4] == 0 and there_is[x - 3][y - 3] == 1 and there_is[x - 2][y - 2] == 1 and \
                    there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 0:
                count_3 += 1

        #대각선_2

        if (x>3 and x<7) and (y>0 and y<4):
            if there_is[x + 1][y - 1] == 0 and there_is[x - 1][y + 1] == 1 and there_is[x - 2][y + 2] == 1 and \
                    there_is[x - 3][y + 3] == 1 and there_is[x - 4][y + 4] == 0:
                count_3 += 1
        if (x>2 and x<6) and (y>1 and y<5):
            if there_is[x + 2][y - 2] == 0 and there_is[x + 1][y - 1] == 1 and there_is[x - 1][y + 1] == 1 and \
                    there_is[x - 2][y + 2] == 1 and there_is[x - 3][y + 3] == 0:
                count_3 += 1
        if (x>1 and x<5) and (y>2 and y<6):
            if there_is[x + 3][y - 3] == 0 and there_is[x + 2][y - 2] == 1 and there_is[x + 1][y - 1] == 1 and \
                    there_is[x - 1][y + 1] == 1 and there_is[x - 2][y + 2] == 0:
                count_3 += 1
        if (x>0 and x<4) and (y>3 and y<7):
            if there_is[x + 4][y - 4] == 0 and there_is[x + 3][y - 3] == 1 and there_is[x + 2][y - 2] == 1 and \
                    there_is[x + 1][y - 1] == 1 and there_is[x - 1][y + 1] == 0:
                count_3 += 1

        #가로
        if (y>0 and y<4):
            if there_is[x][y - 1] == 0 and there_is[x][y + 1] == 1 and there_is[x][y + 2] == 1 and \
                    there_is[x][y + 3] == 1 and there_is[x][y + 4] == 0:
                count_3 += 1
        if (y>1 and y<5):
            if there_is[x][y - 2] == 0 and there_is[x][y - 1] == 1 and there_is[x][y + 1] == 1 and \
                    there_is[x][y + 2] == 1 and there_is[x][y + 3] == 0:
                count_3 += 1
        if (y>2 and y<6):
            if there_is[x][y - 3] == 0 and there_is[x][y - 2] == 1 and there_is[x][y - 1] == 1 and \
                    there_is[x][y + 1] == 1 and there_is[x][y + 2] == 0:
                count_3 += 1
        if (y>3 and y<7):
            if there_is[x][y - 4] == 0 and there_is[x][y - 3] == 1 and there_is[x][y - 2] == 1 and \
                    there_is[x][y - 1] == 1 and there_is[x][y + 1] == 0:
                count_3 += 1
        #세로
        if (x>0 and x<4):
            if there_is[x-1][y]==0 and there_is[x+1][y]==1 and there_is[x+2][y]==1 and there_is[x+3][y]==1 and there_is[x+4][y]==0:
                count_3 +=1
        if (x>1 and x<5):
            if there_is[x - 2][y] == 0 and there_is[x - 1][y] == 1 and there_is[x + 1][y ] == 1 and \
                    there_is[x + 2][y] == 1 and there_is[x + 3][y] == 0:
                count_3 += 1
        if (x>2 and x<6):
            if there_is[x - 3][y] == 0 and there_is[x - 2][y] == 1 and there_is[x - 1][y] == 1 and \
                    there_is[x + 1][y] == 1 and there_is[x + 2][y] == 0:
                count_3 += 1
        if (x>3 and x<7):
            if there_is[x - 4][y] == 0 and there_is[x - 3][y] == 1 and there_is[x - 2][y] == 1 and \
                    there_is[x - 1][y] == 1 and there_is[x + 1][y] == 0:
                count_3 += 1

        if count_3 >=2:
            check=False

        # 4x4

        count_4 =0
        # 대각선_1

        if (x > 0 and x < 3) and (y > 0 and y < 3):
            if there_is[x - 1][y - 1] == 0 and there_is[x + 1][y + 1] == 1 and there_is[x + 2][y + 2] == 1 and \
                    there_is[x + 3][y + 3] == 1 and there_is[x + 4][y + 4] == 1 and there_is[x+5][y+5]==0:
                count_4 += 1
        if (x > 1 and x < 4) and (y > 1 and y < 4):
            if there_is[x - 2][y - 2] == 0 and there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1 and \
                    there_is[x + 2][y + 2] == 1 and there_is[x + 3][y + 3] == 1 and there_is[x+4][y+4]==0:
                count_4 += 1
        if (x > 2 and x < 5) and (y > 2 and y < 5):
            if there_is[x - 3][y - 3] == 0 and there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and \
                    there_is[x + 1][y + 1] == 1 and there_is[x + 2][y + 2] == 1 and there_is[x+3][y+3]==0:
                count_4 += 1
        if (x > 3 and x < 6) and (y > 3 and y < 6):
            if there_is[x - 4][y - 4] == 0 and there_is[x - 3][y - 3] == 1 and there_is[x - 2][y - 2] == 1 and \
                    there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1 and there_is[x+2][y+2]==0:
                count_4 += 1
        if (x > 4 and x < 7) and (y > 4 and y < 7):
            if there_is[x - 5][y - 5] == 0 and there_is[x - 4][y - 4] == 1 and there_is[x - 3][y - 3] == 1 and \
                    there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and there_is[x+1][y+1]==0:
                count_4 += 1

        # 대각선_2

        if (x > 4 and x < 7) and (y > 0 and y < 3):
            if there_is[x + 1][y - 1] == 0 and there_is[x - 1][y + 1] == 1 and there_is[x - 2][y + 2] == 1 and \
                    there_is[x - 3][y + 3] == 1 and there_is[x - 4][y + 4] == 1 and there_is[x-5][y+5]==0:
                count_4 += 1
        if (x > 3 and x < 6) and (y > 1 and y < 4):
            if there_is[x + 2][y - 2] == 0 and there_is[x + 1][y - 1] == 1 and there_is[x - 1][y + 1] == 1 and \
                    there_is[x - 2][y + 2] == 1 and there_is[x - 3][y + 3] == 1 and there_is[x-4][y+4]==0:
                count_4 += 1
        if (x > 2 and x < 5) and (y > 2 and y < 5):
            if there_is[x + 3][y - 3] == 0 and there_is[x + 2][y - 2] == 1 and there_is[x + 1][y - 1] == 1 and \
                    there_is[x - 1][y + 1] == 1 and there_is[x - 2][y + 2] == 1 and there_is[x-3][y+3]==0:
                count_4 += 1
        if (x > 1 and x < 4) and (y > 3 and y < 6):
            if there_is[x + 4][y - 4] == 0 and there_is[x + 3][y - 3] == 1 and there_is[x + 2][y - 2] == 1 and \
                    there_is[x + 1][y - 1] == 1 and there_is[x - 1][y + 1] == 1 and there_is[x-2][y+2]==0:
                count_4 += 1
        if (x > 0 and x < 3) and (y > 4 and y < 7):
            if there_is[x + 5][y - 5] == 0 and there_is[x + 4][y - 4] == 1 and there_is[x + 3][y - 3] == 1 and \
                    there_is[x + 2][y - 2] == 1 and there_is[x + 1][y - 1] == 0 and there_is[x-1][y+1]==0:
                count_4 += 1

        # 가로
        if (y > 0 and y < 3):
            if there_is[x][y - 1] == 0 and there_is[x][y + 1] == 1 and there_is[x][y + 2] == 1 and \
                    there_is[x][y + 3] == 1 and there_is[x][y + 4] == 1 and there_is[x][y + 5] == 0:
                count_4 += 1
        if (y > 1 and y < 4):
            if there_is[x][y - 2] == 0 and there_is[x][y - 1] == 1 and there_is[x][y + 1] == 1 and \
                    there_is[x][y + 2] == 1 and there_is[x][y + 3] == 1 and there_is[x][y + 4] == 0:
                count_4 += 1
        if (y > 2 and y < 5):
            if there_is[x][y - 3] == 0 and there_is[x][y - 2] == 1 and there_is[x][y - 1] == 1 and \
                    there_is[x][y + 1] == 1 and there_is[x][y + 2] == 1 and there_is[x][y + 3] == 0:
                count_4 += 1
        if (y > 3 and y < 6):
            if there_is[x][y - 4] == 0 and there_is[x][y - 3] == 1 and there_is[x][y - 2] == 1 and \
                    there_is[x][y - 1] == 1 and there_is[x][y + 1] == 1 and there_is[x][y + 2] == 0:
                count_4 += 1
        if (y > 4 and y < 7):
            if there_is[x][y - 5] == 0 and there_is[x][y - 4] == 1 and there_is[x][y - 3] == 1 and \
                    there_is[x][y - 2] == 1 and there_is[x][y - 1] == 1 and there_is[x][y + 1] == 0:
                count_4 += 1
        # 세로
        if (x > 0 and x < 3):
            if there_is[x - 1][y] == 0 and there_is[x + 1][y] == 1 and there_is[x + 2][y] == 1 and \
                    there_is[x + 3][y] == 1 and there_is[x + 4][y] == 1 and there_is[x + 5][y] == 0:
                count_4 += 1
        if (x > 1 and x < 4):
            if there_is[x - 2][y] == 0 and there_is[x - 1][y] == 1 and there_is[x + 1][y] == 1 and \
                    there_is[x + 2][y] == 1 and there_is[x + 3][y] == 1 and there_is[x + 4][y] == 0:
                count_4 += 1
        if (x > 2 and x < 5):
            if there_is[x - 3][y] == 0 and there_is[x - 2][y] == 1 and there_is[x - 1][y] == 1 and \
                    there_is[x + 1][y] == 1 and there_is[x + 2][y] == 1 and there_is[x + 3][y] == 0:
                count_4 += 1
        if (x > 3 and x < 6):
            if there_is[x - 4][y] == 0 and there_is[x - 3][y] == 1 and there_is[x - 2][y] == 1 and \
                    there_is[x - 1][y] == 1 and there_is[x + 1][y] == 1 and there_is[x + 2][y] == 0:
                count_4 += 1
        if (x > 4 and x < 7):
            if there_is[x - 5][y] == 0 and there_is[x - 4][y] == 1 and there_is[x - 3][y] == 1 and \
                    there_is[x - 2][y] == 1 and there_is[x - 1][y] == 1 and there_is[x + 1][y] == 0:
                count_4 += 1

        if count_4 >=2:
            check=False

        # 장목 6목
        
        # 대각선 좌측 상향

        if (y > 0 and y < 4)  and (x > 0 and x < 4):

            if there_is[x-1][y - 1] == 1 and there_is[x+1][y + 1] == 1 and there_is[x+2][y + 2] == 1 and there_is[x+3][y + 3] == 1 and there_is[x+4][y + 4] == 1:
                check = False

        elif (y > 1 and y < 5) and (x > 1 and x < 5):

            if there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1 and there_is[x + 2][y + 2] == 1 and there_is[x + 3][y + 3] == 1:
                check = False

        elif (y > 2 and y < 6) and (x > 2 and x < 6):
            if there_is[x - 3][y - 3] == 1 and there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1 and there_is[x + 2][y + 2] == 1:
                check = False

        elif (y > 3 and y < 7) and (x > 3 and x < 7):
            if there_is[x - 4][y - 4] == 1 and there_is[x - 3][y - 3] == 1 and there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1:
                check = False

        # 대각선 우측 상향

        if (y > 3 and y < 7)  and (x > 0 and x < 4):

            if there_is[x+4][y - 4] == 1 and there_is[x+3][y -3] == 1 and there_is[x+2][y - 2] == 1 and there_is[x+1][y -1] == 1 and there_is[x-1][y + 1] == 1:
                check = False

        elif (y > 2 and y < 6) and (x > 1 and x < 5):

            if there_is[x + 3][y - 3] == 1 and there_is[x + 2][y - 2] == 1 and there_is[x + 1][y - 1] == 1 and there_is[x + 1][y - 1] == 1 and there_is[x + 2][y - 2] == 1:
                check = False

        elif (y > 1 and y < 5) and (x > 2 and x < 6):
            if there_is[x + 2][y - 2] == 1 and there_is[x + 1][y - 1] == 1 and there_is[x - 1][y + 1] == 1 and \
                    there_is[x - 2][y + 2] == 1 and there_is[x - 3][y + 3] == 1:
                check = False

        elif (y > 0 and y < 4) and (x > 3 and x < 7):
            if there_is[x + 1][y - 1] == 1 and there_is[x - 1][y + 1] == 1 and there_is[x - 2][y + 2] == 1 and \
                there_is[x - 3][y + 3] == 1 and there_is[x - 4][y + 4] == 1:
                check = False


        # 가로

        if y > 0 and y < 4:

            if there_is[x][y - 1] == 1 and there_is[x][y + 1] == 1 and there_is[x][y + 2] == 1 and there_is[x][
                y + 3] == 1 and there_is[x][y + 4] == 1:
                check = False

        elif y > 1 and y < 5:

            if there_is[x][y - 2] == 1 and there_is[x][y - 1] == 1 and there_is[x][y + 1] == 1 and there_is[x][y + 2] == 1 and there_is[x][y + 3] == 1:
                check = False

        elif y > 2 and y < 6:

            if there_is[x][y - 3] == 1 and there_is[x][y - 2] == 1 and there_is[x][y - 1] == 1 and there_is[x][y + 1] == 1 and there_is[x][y + 2] == 1:
                check = False

        elif y > 3 and y < 7:

            if there_is[x][y - 4] == 1 and there_is[x][y - 3] == 1 and there_is[x][y - 2] == 1 and there_is[x][y - 1] == 1 and there_is[x][y + 1] == 1:
                check = False

        # 세로

        if x > 0 and x < 4:
            if there_is[x - 1][y] == 1 and there_is[x + 1][y] == 1 and there_is[x + 2][y] == 1 and there_is[x + 3][y] == 1 and there_is[x + 4][y] == 1:
                check = False

        elif x > 1 and x < 5:
            if there_is[x - 2][y] == 1 and there_is[x - 1][y] == 1 and there_is[x + 1][y] == 1 and there_is[x + 2][y] == 1 and there_is[x + 3][y] == 1:
                check = False
        elif x > 2 and x < 6:

            if there_is[x - 3][y] == 1 and there_is[x - 2][y] == 1 and there_is[x - 1][y] == 1 and there_is[x + 1][y] == 1 and there_is[x + 2][y] == 1:
                check = False

        elif x > 3 and x < 7:

            if there_is[x - 4][y] == 1 and there_is[x - 3][y] == 1 and there_is[x - 2][y] == 1 and there_is[x - 1][y] == 1 and there_is[x + 1][y] == 1:
                check = False

        # 장목 7목

        #가로
        if y < 4 and y > 1:
            if there_is[x][y-2]==1 and there_is[x][y-1]==1 and there_is[x][y+1]==1 and there_is[x][y+2]==1 and there_is[x][y+3]==1 and there_is[x][y+4]==1:
                check=False
        elif y<5 and y>2:
            if there_is[x][y-3]==1 and there_is[x][y-2]==1 and there_is[x][y-1]==1 and there_is[x][y+1]==1 and there_is[x][y+2]==1 and there_is[x][y+3]==1:
                check=False
        elif y<6 and y>3:
            if there_is[x][y-4]==1 and there_is[x][y-3]==1 and there_is[x][y-2]==1 and there_is[x][y-1]==1 and there_is[x][y+1]==1 and there_is[x][y+2]==1:
                check=False



        #세로
        if x < 4 and x > 1:
            if there_is[x-2][y]==1 and there_is[x-1][y]==1 and there_is[x+1][y]==1 and there_is[x+2][y]==1 and there_is[x+3][y]==1 and there_is[x+4][y]==1:
                check=False
        elif x<5 or x>2:
            if there_is[x-3][y]==1 and there_is[x-2][y]==1 and there_is[x-1][y]==1 and there_is[x+1][y]==1 and there_is[x+2][y]==1 and there_is[x+3][y]==1:
                check=False
        elif x<6 and x>3:
            if there_is[x-4][y]==1 and there_is[x-3][y]==1 and there_is[x-2][y]==1 and there_is[x-1][y]==1 and there_is[x+1][y]==1 and there_is[x+2][y]==1:
                check=False
        # 대각선 좌측상향

        if (y > 1 and y < 4) and (x > 1 and x < 4):

            if there_is[x -2][y -2] == 1and there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1 and there_is[x + 2][y + 2] == 1 and \
                    there_is[x + 3][y + 3] == 1 and there_is[x + 4][y + 4] == 1 :
                check = False

        elif (y > 2 and y < 5) and (x > 2 and x < 5):

            if there_is[x - 3][y - 3] == 1 and there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and there_is[x + 1][y + 1] == 1 and \
                    there_is[x + 2][y + 2] == 1 and there_is[x + 3][y + 3] == 1:
                check = False

        elif (y > 3 and y < 6) and (x > 3 and x < 6):
            if there_is[x - 4][y - 4] == 1 and there_is[x - 3][y - 3] == 1 and there_is[x - 2][y - 2] == 1 and there_is[x - 1][y - 1] == 1 and \
                    there_is[x + 1][y + 1] == 1 and there_is[x + 2][y + 2] == 1:
                check = False

        # 대각선 우측 상향

        if (y > 3 and y < 6)  and (x > 1 and x < 4):

            if there_is[x+4][y - 4] == 1 and there_is[x+3][y -3] == 1 and there_is[x+2][y - 2] == 1 and there_is[x+1][y -1] == 1 and there_is[x-1][y + 1] == 1 and there_is[x + 2][y - 2] == 1:
                check = False

        elif (y > 2 and y < 5) and (x > 2 and x < 5):

            if there_is[x + 3][y - 3] == 1 and there_is[x + 2][y - 2] == 1 and there_is[x + 1][y - 1] == 1 and there_is[x + 1][y - 1] == 1 and there_is[x + 2][y - 2] == 1 and there_is[x - 3][y + 3] == 1:
                check = False

        elif (y > 1 and y < 4) and (x > 3 and x < 6):
            if there_is[x + 2][y - 2] == 1 and there_is[x + 1][y - 1] == 1 and there_is[x - 1][y + 1] == 1 and \
                    there_is[x - 2][y + 2] == 1 and there_is[x - 3][y + 3] == 1 and there_is[x - 4][y + 4] == 1:
                check = False



        
        # 장목 8목
        #대각선
        if x==3 and y==3 and there_is[0][0] ==1 and there_is[1][1]==1 and there_is[2][2]==1 and there_is[4][4]==1 and there_is[5][5]==1 and there_is[6][6]==1 and there_is[7][7]==1:
            check=False
        if x==4 and y==4 and there_is[0][0] ==1 and there_is[1][1]==1 and there_is[2][2]==1 and there_is[3][3]==1 and there_is[5][5]==1 and there_is[6][6]==1 and there_is[7][7]==1:
            check=False
        if x==3 and y==4 and there_is[0][7] ==1 and there_is[1][6]==1 and there_is[2][5]==1 and there_is[4][3]==1 and there_is[5][2]==1 and there_is[6][1]==1 and there_is[7][0]==1:
            check=False
        if x==4 and y==3 and there_is[0][7] ==1 and there_is[1][6]==1 and there_is[2][5]==1 and there_is[3][4]==1 and there_is[5][2]==1 and there_is[6][1]==1 and there_is[7][0]==1:
            check=False
        # 가로
        if y == 4 and there_is[x][0]==1 and there_is[x][1]==1 and there_is[x][2]==1 and there_is[x][3]==1 and there_is[x][5]==1 and there_is[x][6]==1 and there_is[x][7]==1:
            check = False
        if y==3 and there_is[x][0]==1 and there_is[x][1]==1 and there_is[x][2]==1 and there_is[x][4]==1 and there_is[x][5]==1 and there_is[x][6]==1 and there_is[x][7]==1:
            check = False
        # 세로
        if x==4 and there_is[0][y]==1 and there_is[1][y]==1 and there_is[2][y]==1 and there_is[3][y]==1 and there_is[5][y]==1 and there_is[6][y]==1 and there_is[7][y]==1:
            check = False
        if x == 3 and there_is[0][y]==1 and there_is[1][y]==1 and there_is[2][y]==1 and there_is[4][y]==1 and there_is[5][y]==1 and there_is[6][y]==1 and there_is[7][y]==1:
            check = False

    return check



#승리 조건 체크

def winner(there_is):

    win=0

    # 좌측 대각선
    for i in range(4):
        for j in range(4):
            if there_is[i][j] == 1 and there_is[i+1][j+1]== 1 and there_is[i+2][j+2]== 1 and there_is[i+3][j+3]== 1 and there_is[i+4][j+4]== 1:
                win = 1
                return win
            elif there_is[i][j] == 2 and there_is[i+1][j+1]== 2 and there_is[i+2][j+2]== 2 and there_is[i+3][j+3]== 2 and there_is[i+4][j+4]== 2:
                win =2
                return win

    # 우측 대각선

    for i in range(4):
        for j in range(4,8):
            if there_is[i][j] == 1 and there_is[i+1][j-1]== 1 and there_is[i+2][j-2]== 1 and there_is[i+3][j-3]== 1 and there_is[i+4][j-4]== 1:
                win = 1
                return win
            elif there_is[i][j] == 1 and there_is[i+1][j-1]== 1 and there_is[i+2][j-2]== 1 and there_is[i+3][j-3]== 1 and there_is[i+4][j-4]== 1:
                win = 2
                return win


    #가로
    for i in range(8):
        for j in range(4):
            if there_is[i][j] == 1 and there_is[i][j+1]== 1 and there_is[i][j+2]== 1 and there_is[i][j+3]== 1 and there_is[i][j+4]== 1:
                win = 1
                return win
            elif there_is[i][j] == 2 and there_is[i][j+1]== 2 and there_is[i][j+2]== 2 and there_is[i][j+3]== 2 and there_is[i][j+4]== 2:
                win =2
                return win

    #세로
    for i in range(4):
        for j in range(8):
            if there_is[i][j] == 1 and there_is[i+1][j]== 1 and there_is[i+2][j]== 1 and there_is[i+3][j]== 1 and there_is[i+4][j]== 1:
                win = 1
                return win
            elif there_is[i][j] == 2 and there_is[i+1][j]== 2 and there_is[i+2][j]== 2 and there_is[i+3][j]== 2 and there_is[i+4][j]== 2:
                win =2
                return win

    return win


# 시작메뉴
def mainmenu():
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gameDisplay.blit(mainmenu_background, (0, 0))
        Button(mainmenu_start, 405, 250, 150, 80, mainmenu_start_click, 380, 235, selectPlay)
        Button(mainmenu_explain, 370, 350, 230, 80, mainmenu_explain_click, 380, 335, explain)
        Button(mainmenu_finish, 360, 450, 300, 80, mainmenu_finish_click, 380, 435, finishgame)

        pygame.display.update()
        clock.tick(15)


# 1P로 할지 2P로 할지 선택
def selectPlay():
    play = True

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(mainmenu_background, (0, 0))
        Button(player_1P, 405, 250, 150, 80, player_1P, 380, 235, selectStone)
        Button(player_2P, 405, 350, 150, 80, player_2P, 380, 335, gamePvP)

        pygame.display.update()
        clock.tick(15)


# 검정으로 할지 흰색으로 할지 선택
def selectStone():
    play = True

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(mainmenu_background, (0, 0))
        Button(player_blackPlayer, 280, 250, 350, 80, player_blackPlayer, 300, 235, gamePvE)
        Button(player_whitePlayer, 280, 350, 350, 80, player_whitePlayer, 300, 335, gameEvP)

        pygame.display.update()
        clock.tick(15)





# Player vs Player
def gamePvP():
    gameexit = False
    player_turn = 1

    while not gameexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        count_player1 = 0
        count_player2 = 0
        gameDisplay.blit(game_background, (0, 0))
        gameDisplay.blit(game_player_turn, (670, 0))

        # 말 그림 놓기
        for i in range(8):
            for j in range(8):
                if there_is[i][j] == 1:
                    gameDisplay.blit(game_player1, (53 + (i * 70), 50 + (j * 70)))
                    count_player1 += 1
                elif there_is[i][j] == 2:
                    gameDisplay.blit(game_player2, (53 + (i * 70), 50 + (j * 70)))
                    count_player2 += 1


        if player_turn == 1:  # 1P 턴일 때
            gameDisplay.blit(game_player1, (760, 170))
            player1 = Player(game_player1, player_turn)
            player_turn = player1.turn
        else:  # 2P 턴일 때
            gameDisplay.blit(game_player2, (760, 170))
            player2 = Player(game_player2, player_turn)
            player_turn = player2.turn
        pygame.display.update()

        if winner(there_is)==1:
            gameDisplay.blit(game_finish, (150, 100))
            gameDisplay.blit(game_player1, (450, 300))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()
        elif winner(there_is)==2:
            gameDisplay.blit(game_finish, (150, 100))
            gameDisplay.blit(game_player2, (450, 300))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()
        elif count_player1 + count_player2 == 64:
            gameDisplay.blit(game_finish_draw, (150, 100))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()

        clock.tick(30)


# Player:흰색 CPU:검정
def gameEvP():
    gameexit = False
    player_turn = 1
    while not gameexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        count_player1 = 0
        count_player2 = 0
        gameDisplay.blit(game_background, (0, 0))
        gameDisplay.blit(game_player_turn, (670, 0))

        # 말 그림 놓기
        for i in range(8):
            for j in range(8):
                if there_is[i][j] == 1:
                    gameDisplay.blit(game_player1, (53 + (i * 70), 50 + (j * 70)))
                    count_player1 += 1
                elif there_is[i][j] == 2:
                    gameDisplay.blit(game_player2, (53 + (i * 70), 50 + (j * 70)))
                    count_player2 += 1


        if player_turn == 1:  # 1P 턴일 때
            gameDisplay.blit(game_player1, (760, 170))
            player1 = CPU(game_player1, player_turn)
            player_turn = player1.turn
        else:  # 2P 턴일 때
            gameDisplay.blit(game_player2, (760, 170))
            player2 = Player(game_player2, player_turn)
            player_turn = player2.turn
        pygame.display.update()

        if winner(there_is) == 1:
            gameDisplay.blit(game_finish, (150, 100))
            gameDisplay.blit(game_player1, (450, 300))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()
        elif winner(there_is) == 2:
            gameDisplay.blit(game_finish, (150, 100))
            gameDisplay.blit(game_player2, (450, 300))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()
        elif count_player1 + count_player2 == 64:
            gameDisplay.blit(game_finish_draw, (150, 100))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()

        clock.tick(30)


# Player:검정 CPU:흰색
def gamePvE():
    gameexit = False
    player_turn = 1

    while not gameexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        count_player1 = 0
        count_player2 = 0
        gameDisplay.blit(game_background, (0, 0))
        gameDisplay.blit(game_player_turn, (670, 0))


        # 말 그림 놓기
        for i in range(8):
            for j in range(8):
                if there_is[i][j] == 1:
                    gameDisplay.blit(game_player1, (53 + (i * 70), 50 + (j * 70)))
                    count_player1 += 1
                elif there_is[i][j] == 2:
                    gameDisplay.blit(game_player2, (53 + (i * 70), 50 + (j * 70)))
                    count_player2 += 1


        if player_turn == 1:  # 1P 턴일 때
            gameDisplay.blit(game_player1, (760, 170))
            player1 = Player(game_player1, player_turn)
            player_turn = player1.turn
        else:  # 2P 턴일 때
            gameDisplay.blit(game_player2, (760, 170))
            player2 = CPU(game_player2, player_turn)
            player_turn = player2.turn
        pygame.display.update()

        if winner(there_is) == 1:
            gameDisplay.blit(game_finish, (150, 100))
            gameDisplay.blit(game_player1, (450, 300))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()
        elif winner(there_is) == 2:
            gameDisplay.blit(game_finish, (150, 100))
            gameDisplay.blit(game_player2, (450, 300))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()
        elif count_player1 + count_player2 == 64:
            gameDisplay.blit(game_finish_draw, (150, 100))
            pygame.display.update()
            time.sleep(5)
            reset()
            mainmenu()

        clock.tick(30)


# 게임 판 초기화
def reset():
    for i in range(8):
        for j in range(8):
            there_is[i][j] = 0

# 설명
def explain():
    exp = True

    while exp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(explain_background, (0, 0))
        Button(explain_back, 670, 560, 230, 140, explain_back_click, 660, 540, mainmenu)

        pygame.display.update()
        clock.tick(15)


# 게임 종료
def finishgame():
    pygame.quit()
    sys.exit()


mainmenu()
game()
