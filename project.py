############# IMPORTS #################

import pygame, random, csv, threading, time, sys, os, math
from pygame import mixer
from threading import Timer
from pygame.locals import *
from chatbot_module import ChatbotLevel, first_level
clock = pygame.time.Clock()
pygame.init()


########### SET UP #########################   
           
WIDTH = 1000 #game window width
HEIGHT = 500 #game window height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#colours
font = pygame.font.SysFont("Helvetica", 25)
font2 = pygame.font.SysFont("Aharoni", 30)
BLACK = [0, 0, 0]
TEAL = [133, 167, 229]
BLUE = [0, 102, 102]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREY = [211, 211, 211]
DARKGREY = [100, 100, 100]

############## GLOBAL SPRITES ######################

### walking dino buffer to circulate and make it look like its moving
player_images = []
player_images.append( pygame.image.load('dinowalking1.jpg') )
player_images.append( pygame.image.load('dinowalking2.jpg') )
player_current = 0
player = player_images[ player_current ]

playerX = 610
playerY = 350

walking = False
walking_steps = 0

##Background
BGImg = pygame.image.load("Level1-street.png")
BGImg = pygame.transform.scale(BGImg, (WIDTH, HEIGHT ))



##Screens
displayWidth, displayHeight = WIDTH, HEIGHT
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
titleImg = pygame.image.load("startpage.png")
titleImg = pygame.transform.scale(titleImg, (displayWidth, displayHeight))
EoGImg = pygame.image.load("endofgamescreen.png") 
EoGImg = pygame.transform.scale(EoGImg, (displayWidth, displayHeight))
titleScreen = False


####### TEXT OBJECTS ######################
def textObjects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

initial_convo_text = ["Salut, Hopper!; Hi, Hopper!",
    "Bonjour Dino!; Hello Dino!",
    "Ça va?; How are you? (informal)",
    "Ça va bien! Et toi?; I'm doing well! And you?",
    "Super! Au revior Dino.; Super! Goodbye Dino.",
    "À plus tard!; See you later!"]
current_text_index = 0

fontObj = pygame.font.Font(None, 32)
current_text = ""
textSufaceObj = fontObj.render(initial_convo_text[current_text_index], True, BLACK, None)
textRectObj = textSufaceObj.get_rect()

############### MAKE SHIFT BUTTONS ############################

def button(msg, x, y, w, h, c, action=None):
    # parameters taken - message, x coord, y coord, width, height, colour, action
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, c, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, c, (x, y, w, h))
    text = pygame.font.SysFont("Aharoni", 30)
    textSurf, textRect = textObjects(msg, text)
    textRect.center = ((x+(w/2)), y+(h/2))
    screen.blit(textSurf, textRect)
    


'''
##################### INSTRUCTIONS SCREEN ###################

### Gonna finish this code once we have the actual game set up

def gameInstructions():
    global titleScreen, GameScreen
    titleScreen = False
    GameScreen = True
    while GameScreen == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                titleScreen = False
                quit()
        screen.blit(GameInstructions, (0,0))
        button("Back", 100, 550, 100, 50, TEAL, titleLoop)
        pygame.display.update()
        clock.tick(60)
'''      
    
def quitGame():
    pygame.quit()
    quit()

        
def titleLoop():       
    screen.blit(titleImg, (0,0))
    titleScreen = True
    while titleScreen == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                titleScreen = False
                quit()
        button("Play",  80, 200, 350, 60, TEAL, mainloop)
        pygame.display.update()
        clock.tick(60)


        
def mainloop():

    ####### no clue why the global variables at the start aren't being accessed here]
    ####### if anyone can fix this, slay

    global walking
    walking_forward = False
    walking_backwards = False

    player_images = []
    dino1 =  pygame.image.load('dinowalking1.jpg')
    dino1 = pygame.transform.scale(dino1, (80,80))
    dino2 =  pygame.image.load('dinowalking2.jpg')
    dino2 = pygame.transform.scale(dino2, (80, 80))
    player_images.append(dino1)
    player_images.append(dino2)
    player_current = 0
    player = player_images[ player_current ]

    playerX = 610
    playerY = 350


    global pause
    #rectangle = (0, 40, 1000, 610)


    global score
    score = 0
    timeToBlit = None

    global gameLoop
    gameLoop = True
    while gameLoop==True:
        clock.tick(30)

        # ----------- events -----------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_LEFT:
                    walking_backwards = True
                    walking_forward = False
                    walking_steps = 5
                elif event.key == pygame.K_RIGHT:
                    walking_forward = True
                    walking_backwards = False
                    walking_steps = 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    current_text_index = (current_text_index + 1) % len(initial_convo_text)
                    current_text = initial_convo_text[current_text_index]

        # ---------- moves -----------------
        if walking_forward == True:
        # here you need to check some counter 
        # if it is time for next step to walk slower
        # but don't use `time.sleep()`
            if walking_steps > 0:
                player_current = (player_current + 1) % len(player_images)
                player = player_images[ player_current ]
                playerX = playerX + 3
                walking_steps -= 1
            else:
                walking = False  

        elif walking_backwards == True:
        # here you need to check some counter 
        # if it is time for next step to walk slower
        # but don't use `time.sleep()`
            if walking_steps > 0:
                player_current = (player_current - 1) % len(player_images)
                player = player_images[ player_current ]
                playerX = playerX - 3
                walking_steps -= 1
            else:
                walking = False 
        
        #screen.blit(dinoImg, (dinoX, dinoY))
         
        # --- draws ---

        screen.blit(BGImg, (0,0))
        screen.blit(player, (playerX, playerY))
        screen.blit(textSufaceObj, textRectObj)

        #pygame.display.flip()
        pygame.display.update()
        #clock.tick(60)
        
        
titleLoop()
