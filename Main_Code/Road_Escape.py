import pygame
import random
from sys import exit
import cv2
import mediapipe as mp
import math

pygame.init()

def len(x1,y1, x2, y2):
    return int(pow( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) ,0.5))

    # Initialise the Camera and Mediapipe module
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
line = mp.solutions.drawing_utils

WIDTH = 800
HEIGHT = 600
LANES = 4
WIDTH_OF_LANE = WIDTH/LANES

    #Gaming Window and Background
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('background.png')
    #Title and Icon
pygame.display.set_caption("Road_Escape")
icon = pygame.image.load('flags.png')
pygame.display.set_icon(icon)

    # Player
playerImg = pygame.image.load('car_player.png')
Current_Lane = random.randint(1,LANES)
playerX = (Current_Lane*WIDTH_OF_LANE)-(WIDTH_OF_LANE/2)-32
playerY = 480

score_font = pygame.font.Font('freesansbold.ttf',32)

#Create Start Menu
while True:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))   # Background
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    # Hand Tracking  for reference https://www.youtube.com/watch?v=NZde8Xt78Iw
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    ok = 100
    fingers = 0    # Number of fingers shown
    if result.multi_hand_landmarks:
        for hand_mark in result.multi_hand_landmarks:
            line.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)
            h,w,c = frame.shape
            org_x, org_y = int(hand_mark.landmark[0].x*w), int((hand_mark.landmark[0].y*h))
            lmlist = []
            for id, lm in enumerate(hand_mark.landmark):
                x, y = int(lm.x*w), int((lm.y*h))
                lmlist.append([id,x,y,len(org_x, org_y, x, y)])
                if id%4 == 0 and id > 0 :
                    cv2.circle(frame , (x,y), 10 , (255,0,255) , cv2.FILLED)
            ok = abs(lmlist[8][3]-lmlist[4][3])  # Distance Between Index finger and Thumb
            for i in range(8, 21, 4):
                if lmlist[i][3] > lmlist[i-2][3]:    # Counting Number of fingers Shown
                    fingers+=1
    cv2.putText(frame, "Join Index Finger and Thumb", (250,30), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,255), 2)
    cv2.putText(frame, "To Start the Game", (310,60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,255), 2)
    cv2.putText(frame, str(fingers), (70,70), cv2.FONT_HERSHEY_COMPLEX, 2 , (255,0,0), 3)
    cv2.imshow("Frame",frame)

    def show_message():
        display_message = score_font.render("Press Any Key To Play", True, (255,255,255))
        screen.blit(display_message,(230, 350))
    show_message()
    
    pygame.display.update()
    
    play_game = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            play_game = True
    if ok < 20 :
        play_game = True
    if play_game:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

cv2.destroyAllWindows()
fingers = Current_Lane

while True:
    
    #Enemy
    enemy_SPEED = 8
    enemyImg = []
    enemyX = []
    enemyY = []
    enemy_speed=[]

    #At a time, only one enemy in a lane
    # Random Spawing of Enemy
    for i in range(LANES+1):
        enemyImg.append(pygame.image.load('car_enemy.png'))
        enemyX.append((i*WIDTH_OF_LANE)-(WIDTH_OF_LANE/2)-32)
        enemyY.append(-200*random.randint(1,12))
        enemy_speed.append(enemy_SPEED)

    #score
    score1 = 0
    score2 = 0
    textX=10
    textY=10

    #Game over text
    game_over = False
    game_over_font = pygame.font.Font('freesansbold.ttf',64)

    def show_score(x, y):
        display_score = score_font.render("Score : " + str(score1), True, (255,255,255))
        screen.blit(display_score,(x, y))
    def game_over_text():
        over_text = game_over_font.render("GAME OVER", True, (255,255,255))
        screen.blit(over_text,(200, 250))
        def show_message():
            display_message_1 = score_font.render("Press Any Key To Play", True, (255,255,255))
            screen.blit(display_message_1,(230, 350))
            display_message_2 = score_font.render("Or", True, (255,255,255))
            screen.blit(display_message_2,(380, 400))
            display_message_3 = score_font.render("Join Index Finger and Thumb", True, (255,255,255))
            screen.blit(display_message_3,(160, 450))
        show_message()
    show_message()
    def enter_to_play():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return True
        return False
    def player(x, y):
        screen.blit(playerImg, (x, y))
    def enemy(x, y,i):
        screen.blit(enemyImg[i], (x, y))
        for j in range(LANES + 1):
            enemy_speed[i] = enemy_SPEED
    def isCollision(enemyY, playerY, i):
        distance = abs(enemyY-playerY)
        if distance < 50 and Current_Lane == i:
            return True
        else:
            return False
    
    #Game Loop
    single_press = False

    while True:
        #RGB
        screen.fill((0,0,0))
        screen.blit(background,(0,0))    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # if a keystroke is pressed check whether its right or left 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if Current_Lane > 1 and single_press == False:
                        Current_Lane -=1
                        single_press = True
                if event.key == pygame.K_RIGHT:
                    if Current_Lane < LANES and single_press == False:
                        Current_Lane +=1
                        single_press = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    single_press = False

            playerX = (Current_Lane*WIDTH_OF_LANE)-(WIDTH_OF_LANE/2)-32 

        #Enemy Movement
        for i in [1,2,3,4]:
            #Game Over
            if isCollision(enemyY[i], playerY, i):
                for j in range(LANES+1):
                    enemyY[j] = 2000
                game_over = True
                break
         
            enemyY[i]+=enemy_speed[i]
        
            if enemyY[i] > HEIGHT and enemyY[i] < 1200:
                score1 += 1
                if score1-score2 > 10:
                    enemy_SPEED += 2
                    score2 = score1
                enemyY[i] = -200*random.randint(0,12)
            enemy(enemyX[i], enemyY[i], i) 

        # Player Movement using Number of fingers shown
        if fingers > 0:
            playerX = 68 + 200*(fingers-1)
            Current_Lane = fingers
        player(playerX, playerY)
        show_score(textX,textY)
        
        # Hand Tracking  for reference https://www.youtube.com/watch?v=NZde8Xt78Iw
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)
        ok = 100
        fingers = 0    # Number of fingers shown
        if result.multi_hand_landmarks:
            for hand_mark in result.multi_hand_landmarks:
                line.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)
                h,w,c = frame.shape
                org_x, org_y = int(hand_mark.landmark[0].x*w), int((hand_mark.landmark[0].y*h))
                lmlist = []
                for id, lm in enumerate(hand_mark.landmark):
                    x, y = int(lm.x*w), int((lm.y*h))
                    lmlist.append([id,x,y,len(org_x, org_y, x, y)])
                    if id%4 == 0 and id > 4:
                        cv2.circle(frame , (x,y), 10 , (255,0,255) , cv2.FILLED)
                ok = abs(lmlist[8][3]-lmlist[4][3])     # Distance Between Index finger and Thumb
                for i in range(8, 21, 4):
                    if lmlist[i][3] > lmlist[i-2][3]:   # Counting Number of fingers Shown
                        fingers+=1
        cv2.putText(frame, str(fingers), (70,70), cv2.FONT_HERSHEY_COMPLEX, 2 , (255,0,0), 3)
        cv2.imshow("Frame",frame)
        if game_over:
            game_over_text()                   # After Game Over restart Game
            if enter_to_play() or ok < 20:     # With Key Press or Joining Index Finger and Thumb
                break
        pygame.display.update()
    # Reinitialising all the variables to restart the game
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    enemy_speed.clear()
