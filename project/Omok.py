import pygame
import time
import sys
import random

# standard gomoku 규칙

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
pygame.display.set_caption("Othello")  # 타이틀
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
                            there_is[i][j] = 1
                            self.turn = 2
                    elif click[0] and turn == 2:  # 2P가 빈자리를 클릭
                            there_is[i][j] = 2
                            self.turn = 1


class CPU:  # 플레이어 행동
    def __init__(self, img, turn):
        self.turn = turn
        able = []

        pygame.display.update()

        time.sleep(0.5)

        for i in range(8):
            for j in range(8):
                if there_is[i][j] == 0:
                    if turn == 1:  # AI가 1P일때
                            able.append([i, j])
                    elif turn == 2:  # AI가 2P일때
                            able.append([i, j])
        if len(able) == 0:
            if turn == 1:
                self.turn = 2
                time.sleep(0.5)
            elif turn == 2:
                self.turn = 1
                time.sleep(0.5)
        else:
            index = random.randrange(len(able))  # 가능한 자리 중 무작위 자리 선정
            i = able[index][0]
            j = able[index][1]
            if turn == 1:
                    there_is[i][j] = 1
                    self.turn = 2
            elif turn == 2:
                    there_is[i][j] = 2
                    self.turn = 1


# AI 범위 지정하는 알고리즘 필요

# 규칙 지정하는 알고리즘 필요

# 승리 확인하는 알고리즘 필요

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

        if count_player1 + count_player2 == 64:  # 총 64개의 돌이 놓이면 종료
            gameDisplay.blit(game_finish_draw, (150, 100))
            if count_player1 > count_player2:
                gameDisplay.blit(game_player1, (450, 300))
            elif count_player2 > count_player1:
                gameDisplay.blit(game_player2, (450, 300))
            else:
                gameDisplay.blit(game_player1, (350, 300))
                gameDisplay.blit(game_player2, (550, 300))
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

        if count_player1 + count_player2 == 64:  # 총 64개의 돌이 놓이면 종료
            gameDisplay.blit(game_finish, (150, 100))
            if count_player1 > count_player2:
                gameDisplay.blit(game_player1, (450, 300))
            elif count_player2 > count_player1:
                gameDisplay.blit(game_player2, (450, 300))
            else:
                gameDisplay.blit(game_player1, (350, 300))
                gameDisplay.blit(game_player2, (550, 300))
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

        if count_player1 + count_player2 == 64:  # 총 64개의 돌이 놓이면 종료
            gameDisplay.blit(game_finish, (150, 100))
            if count_player1 > count_player2:
                gameDisplay.blit(game_player1, (450, 300))
            elif count_player2 > count_player1:
                gameDisplay.blit(game_player2, (450, 300))
            else:
                gameDisplay.blit(game_player1, (350, 300))
                gameDisplay.blit(game_player2, (550, 300))
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
