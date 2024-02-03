############# IMPORTS #################

import pygame, random, csv, threading, time, sys, os, math
from pygame import mixer
from pygame.locals import *
clock = pygame.time.Clock()
pygame.init()


########### SET UP #########################   
           
WIDTH = 1000 #game window width
HEIGHT = 500 #game window height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#colours
font = pygame.font.SysFont("VT323-Regular", 25)

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
player_images.append( pygame.image.load('dinowalk1.png') )
player_images.append( pygame.image.load('dinowalk2.png') )
player_current = 0
player = player_images[ player_current ]

hopper = pygame.image.load("hopper.png")
hopper = pygame.transform.scale(hopper, (80, 80))
hopperRect = hopper.get_rect()

# Load, scale, and add the second bunny sprite
mopper = pygame.image.load("mopper.png")
mopper = pygame.transform.scale(mopper, (80, 80))  # Adjust the size as needed



playerX = 200
playerY = 350

walking = False
walking_steps = 0

dinoGroup = pygame.sprite.GroupSingle(None)  # single group as only one player
bunnyGroup = pygame.sprite.GroupSingle(None)  # group containing all sprites (for updating them in one go)

##Background
BGImg = pygame.image.load("Level2-eiffel.png")
BGImg = pygame.transform.scale(BGImg, (WIDTH, HEIGHT ))
eiffelTower = pygame.image.load("eiffeltower.png")
eiffelTower = pygame.transform.scale(eiffelTower, (180, 300))
BGImg2 = pygame.image.load("Level1-street.png")
BGImg2 = pygame.transform.scale(BGImg2, (WIDTH, HEIGHT ))

##Screens
displayWidth, displayHeight = WIDTH, HEIGHT
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
titleImg = pygame.image.load("startscrn.png")
titleImg = pygame.transform.scale(titleImg, (displayWidth, displayHeight))
#EoGImg = pygame.image.load("endofgamescreen.png")
#EoGImg = pygame.transform.scale(EoGImg, (displayWidth, displayHeight))
titleScreen = False


####### TEXT OBJECTS ######################

def textObjects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()
    

############### MAKE SHIFT BUTTONS ############################

def button(msg, x, y, w, h, c, action=None):

    font_path = "VT323-Regular.ttf"  # Replace with the actual path to VT323.ttf on your system
    font_size = 36
    font = pygame.font.Font(font_path, font_size)

    # Create a text surface
    # parameters taken - message, x coord, y coord, width, height, colour, action
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    border_rect = pygame.Rect(x-5, y-5, w+10, h+10)
    pygame.draw.rect(screen, (255, 255, 255), border_rect)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, c, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, c, (x, y, w, h))
    text = font.render(msg, True, (255, 255, 255))
    textRect = text.get_rect()
    #textSurf, textRect = textObjects(msg, text)
    textRect.center = ((x+(w/2)), y+(h/2))
    screen.blit(text, textRect)
    


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
        button("Play",  320, 200, 350, 60, TEAL, mainloop)
        pygame.display.update()
        clock.tick(60)

def colCheck(x,y,w,h,x2,y2,w2,h2):
#checks if two sprites have met up by comparing the pixel space by comparing their coordinates
    global collision
    collision = False
    if (x < (x2 + w2) and (x + w) > x2 and y < (y2 + h2) and (h + y) > y2):
        collision = True


class Dino(pygame.sprite.Sprite):
    def __init__(self, image_path, position, dimensions):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect(center=position)
    
    def update(self, x, y):
        # Update the sprite's position.
        self.rect.x = x
        self.rect.y = y


class Bunny(pygame.sprite.Sprite):
    def __init__(self, image_path, position, dimensions):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect(center=position)


######### messages ################
# Define messages for the conversation
messages = [
    "Bunny One: Message 1",
    "Bunny Two: Message 2",
    "Bunny One: Message 3",
    "Bunny Two: Message 4"
]
current_message_index = 0  # To keep track of which message to display

# Function to go to the next message
def next_message():
    global current_message_index
    current_message_index += 1
    if current_message_index >= len(messages):
        current_message_index = 0  # Loop back to the first message or end conversation

# Modify or ensure your button function can call next_message
# You might have already a way to call a function, just ensure it calls next_message when needed



def mainloop():

    ####### no clue why the global variables at the start aren't being accessed here]
    ####### if anyone can fix this, slay

    global walking
    walking_forward = False
    walking_backwards = False

    player_images = []
    dino1 =  pygame.image.load('dinowalk1.png')
    dino1 = pygame.transform.scale(dino1, (80,80))
    dinoRect1 = dino1.get_rect()
    dino2 =  pygame.image.load('dinowalk2.png')
    dino2 = pygame.transform.scale(dino2, (80, 80))
    dinoRect2 = dino2.get_rect()
    hopper = pygame.image.load("hopper.png")
    hopper = pygame.transform.scale(hopper, (80, 80))
    hopperRect = hopper.get_rect()
    topper = pygame.image.load("topper.png")
    topper = pygame.transform.scale(topper, (80, 80))
    #mopperBunny = Bunny('topper.png', (880, 400), (80, 80))  # Position it next to the first bunny
    #bunnyGroup.add(mopperBunny)
    player_images.append(dino1)
    player_images.append(dino2)
    player_current = 0
    player = player_images[ player_current ]

    playerX = 200
    playerY = 350

    global pause
    #rectangle = (0, 40, 1000, 610)

    global score
    score = 0
    timeToBlit = None

    global gameLoop
    gameLoop = True

    #bunnyGroup.add(hopper)
    #dinoGroup.add(player)
    # Initialize sprite groups
    dinoGroup = pygame.sprite.GroupSingle()
    bunnyGroup = pygame.sprite.Group()

    # Create instances of Dino and Bunny
    dino = Dino('dinowalk1.png', (75, 350), (80, 80))
    bunny = Bunny('hopper.png', (850, 400), (80, 80))
    topper = Bunny('topper.png', (750, 400), (80, 80))

    # Add instances to their respective groups
    dinoGroup.add(dino)
    bunnyGroup.add(bunny)
    bunnyGroup.add(topper)

    #screen.blit(eiffelTower, (50, 10))
    ##### player sprite

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
        # Inside the game loop, after processing movement
        dino.update(playerX, playerY)
         
        # --- draws ---

        screen.blit(BGImg, (0,0))
        screen.blit(eiffelTower, (425, 100))
        screen.blit(player, (playerX, playerY))

        ############# conversation for first two bunnies ####################
        # Inside your game loop, draw the current message
        font = pygame.font.Font("VT323-Regular.ttf", 24)  # Adjust the size as needed
        text_surface = font.render(messages[current_message_index], True, WHITE)
        text_rect = text_surface.get_rect(center=(750, 340))  # Adjust position as needed
        screen.blit(text_surface, text_rect)
        # Inside your game loop, add a button for progressing through messages
        button("Next", 900, 450, 80, 30, TEAL, next_message)  # Adjust position and size as needed

        meetUp = False
        # --- checking for meet up -----
        if pygame.sprite.spritecollideany(dinoGroup.sprite, bunnyGroup):
            print("Collision detected!")

            ##### Define Font for message ###########
            font_path = "VT323-Regular.ttf"  # Replace with the actual path to VT323.ttf on your system
            font_size = 36
            font = pygame.font.Font(font_path, font_size)

            # Create a text surface
            text = font.render("Hello, VT323 Font!", True, (255, 255, 255))
    
            ###### write message
            msg = "Filler Text"
            pygame.draw.rect(screen, WHITE, (10, 450, 950, 40))
            text = font.render(msg, True, (0, 0, 0))
            textRect = text.get_rect()
            #textSurf, textRect = textObjects(msg, text)
            textRect.center = ((10+(950/2)), 450+(40/2))
            screen.blit(text, textRect)
        
        

        for sprite in bunnyGroup:
            sprite.update()  # update each sprite so change position etc.
        

        
        bunnyGroup.draw(screen)
        #pygame.draw.rect(screen, (255, 0, 0), dinoGroup.sprite.rect, 2)  # Draw dino rect in red
        #for bunny in bunnyGroup:
            #pygame.draw.rect(screen, (0, 255, 0), bunny.rect, 2)  # Draw bunny rects in green
        

        #pygame.display.flip()
        pygame.display.update()
        #clock.tick(60)
        
        
titleLoop()
