############# IMPORTS #################

import pygame, random, csv, threading, time, sys, os, math
from pygame import mixer
from pygame.locals import *
# from chatbot_module import ChatbotLevel, first_level, second_level
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


text_input_active = False

lvl_one_convo = ["Say hello to Hopper!", "When you are finished with the conversation, say \"Au Revoir\"!", "Your turn: "]
current_convo_index = 0
user_text =''

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
    



##################### INSTRUCTIONS SCREEN ###################

### Gonna finish this code once we have the actual game set up
'''
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

def display_instructions():
    # Instructions text

    instructions = [
        "Welcome to Dino in Paris!",
        "Instructions:",
        "- Read what the bunny characters on screen are saying.",
        "- Press next to read the next part of their conversation",
        "- Try and work out what the French words mean based on context.",
        "- Answer questions correctly to earn points.",
        "Good luck!",
        "",
        "Press PLAY to start..."
    ]

    vt323_font_path = "VT323-Regular.ttf"  
    vt323_font_size = 30
    vt323_font = pygame.font.Font(vt323_font_path, vt323_font_size)

    y_position = 50
    for line in instructions:
        text = vt323_font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        y_position += 40


def titleLoop():       
    screen.blit(titleImg, (0,0))
    titleScreen = True
    while titleScreen == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                titleScreen = False
                quit()
        
        display_instructions()
        button("Play",  320, 400, 350, 60, TEAL, mainloop)
        pygame.display.update()
        clock.tick(60)


def quitGame():
    pygame.quit()
    quit()

        


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
french_messages = [
    "Salut, Hopper!", 
    "Bonjour, Hopper!", 
    "Au revoir, Hopper!",
    ""]

english_messages = ["Hi, Hopper!",
                    "Hello, Hopper!", 
                    "Goodbye, Hopper!",
                    ""                    ]

# Initialize separate indices for English and French messages
english_message_index = 0
french_message_index = 0

# This variable will toggle between showing English and French messages
show_english = True

# Initialize separate indices for English and French messages
english_message_index = 0
french_message_index = 0

# This variable toggles between showing English and French messages
show_english = True

def next_message():
    global english_message_index, french_message_index, show_english

    if show_english:
        # Increment English message index if not at the end of the list
        if english_message_index < len(english_messages) - 1:
            english_message_index += 1
            pygame.time.delay(1000)
        else:
            # Optional: Reset index or handle completion
            english_message_index = 0  # Or set to len(english_messages) - 1 to stop incrementing
    else:
        # Increment French message index if not at the end of the list
        if french_message_index < len(french_messages) - 1:
            french_message_index += 1
            pygame.time.delay(1000)
        else:
            # Optional: Reset index or handle completion
            french_message_index = 0  # Or set to len(french_messages) - 1 to stop incrementing

    # Toggle between English and French for the next click
    show_english = not show_english


# Modify or ensure your button function can call next_message
# You might have already a way to call a function, just ensure it calls next_message when needed


current_french_message_index = 0
current_english_message_index = 0

def mainloop():
    global current_french_message_index
    global current_english_message_index

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
        
        button("Next", 900, 400, 80, 30, TEAL, next_message)  # Adjust position and size as needed
        # Inside mainloop, where messages are displayed
        font = pygame.font.Font("VT323-Regular.ttf", 24)

        # Determine which message to show based on the indices
        if (english_message_index + french_message_index) % 2 == 0:
            # Show English message above Topper
            message = english_messages[english_message_index]
            message_position = (750, 350)
        else:
            # Show French message above Hopper
            message = french_messages[french_message_index]
            message_position = (850, 350)

        # Render and display the message
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=message_position)
        screen.blit(text_surface, text_rect)


        

        meetUp = False
        # --- checking for meet up -----
        if pygame.sprite.spritecollideany(dinoGroup.sprite, bunnyGroup):

            ##### Define Font for message ###########
            font_path = "VT323-Regular.ttf"  # Replace with the actual path to VT323.ttf on your system
            font_size = 36
            font = pygame.font.Font(font_path, font_size)

            # Create a text surface
            text = font.render("Hello, VT323 Font!", True, (255, 255, 255))
            # write message
            pygame.draw.rect(screen, WHITE, (10, 450, 950, 40))
            space_text = font.render("Press [SPACE] to continue", True, (0, 0, 0))
            space_text_rect = space_text.get_rect()
            space_text_rect.center = (10 + 950 // 2, 450 + 40 // 2)
            screen.blit(space_text, space_text_rect)

            # ...
            global current_convo_index
            global text_input_active
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if current_convo_index != 2:
                            current_convo_index += 1
                            print(current_convo_index)
                        if current_convo_index == 2:
                            os.system("python chatbot_module.py")
            
            # global user_text
            # events = pygame.event.get()
            # if event.type == QUIT:
            #     running = False
            # elif event.type == KEYDOWN:
            #     if text_input_active:
            #         if event.key == K_RETURN:
            #             # Handle Enter key, e.g., submit user_text
            #             print("User input:", user_text)
            #             user_text = ""
            #         elif event.key == K_BACKSPACE:
            #             # Handle Backspace key
            #             user_text = user_text[:-1]
            #         else:
            #             # Handle other key presses
            #             user_text += event.unicode

            # if text_input_active:
            #     user_text_surface = font.render(user_text, True, (255,255,255))
            #     screen.blit(user_text_surface, (10,10))

            else:
                # Draw the conversation message
                msg = lvl_one_convo[current_convo_index]
                pygame.draw.rect(screen, WHITE, (10, 10, 950, 40))
                text = font.render(msg, True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (10 + 950 // 2, 10 + 40 // 2)
                screen.blit(text, textRect)

        for sprite in bunnyGroup:
            sprite.update()  # update each sprite so change position etc.
        
        bunnyGroup.draw(screen)
        #pygame.draw.rect(screen, (255, 0, 0), dinoGroup.sprite.rect, 2)  # Draw dino rect in red
        #for bunny in bunnyGroup:
        #    pygame.draw.rect(screen, (0, 255, 0), bunny.rect, 2)  # Draw bunny rects in green

        #pygame.display.flip()
        pygame.display.update()
        #clock.tick(60)
        
        
titleLoop()
