import pygame
import math
import random
from pygame import mixer  # for adding music and sounds to the game
import time
import numpy as np

# initialize game
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('barn.png')

# Title and Icon
pygame.display.set_caption("Catch The Eggs")
icon = pygame.image.load('hen.png')
pygame.display.set_icon(icon)

# Background music
mixer.music.load('bgmusic.mp3')
mixer.music.play(-1)  # -1: to continuously have the sound

#main menu
mainmenu = np.array([["->","START GAME"],["__","SHOW HIGHEST SCORE"],["__","EXIT"]])
# Font for start point
start_font = pygame.font.Font('freesansbold.ttf', 24)

def show_explanation():
    explanation = start_font.render("SCROLL UP/DOWN AND PRESS ENTER TO SELECT", True, (255,127,80))
    screen.blit(explanation, (50, 50))


# read high_score from file
try:
    with open('highscore.dat') as high_score_file:
        high_score = int(high_score_file.read())
        # Do something with the file
except FileNotFoundError:
    high_score = 0


# Place Hens in screen
henImg = pygame.image.load('hen2.png')
henX0 = 50
henY = 40
henX = []
for i in range(9):
    henX.append(henX0 + i * 80)

def hen():
    # draw 9 hens in the appropriate place
    for i in range(9):
        screen.blit(henImg, (henX[i], henY))



# # egg
# initial_speed = 0.75
# speed_slope =.05

eggImg = pygame.image.load('egg48.png')
# eggX = random.randint(30, 770)
eggX = [random.choice(henX)+25]
eggY = [henY + 40]


def egg(x, y):
    # draw image on the screen
    screen.blit(eggImg, (x, y))


basketIm = pygame.image.load('wicker-basket.png')
basketX = 450
basketY = 530
basketX_change = 0


def basket(x, y):
    screen.blit(basketIm, (x, y))


# Detect catching of egg
def isCaught(eggX, eggY, basketX, basketY):
    distance = math.sqrt(math.pow(eggX - basketX - 8, 2) + math.pow(eggY - basketY + 16, 2))
    if distance < 8:
        return True


# show scores on the screen
font = pygame.font.Font('freesansbold.ttf', 20)

missed_scoreX = 10
missed_scoreY = 10
caught_scoreX = 400
caught_scoreY = 10
caught_score_value = 0
missed_score_value = 0

def show_scores(x, y, x2, y2):
    missed_score = font.render("Number of Missed Eggs: " + str(abs(missed_score_value)), True, (255, 0, 0))
    caught_score = font.render("Number of Collected Eggs: " + str(caught_score_value), True, (0, 255, 0))
    screen.blit(missed_score, (x, y))
    screen.blit(caught_score, (x2, y2))


# Show game over message
over_font = pygame.font.Font('freesansbold.ttf', 64)
over_font_small = pygame.font.Font('freesansbold.ttf', 14)


def game_over():
    over_txt = over_font.render("GAME OVER", True, (0, 250, 194))
    screen.blit(over_txt, (200, 150))
    over_txt_small = over_font_small.render("*Back to main menu in 5 sec", True, (10, 10, 10))
    screen.blit(over_txt_small, (220, 250))


# Game Loop
def game_start():
    global eggY, basketX_change, basketX, eggX, caught_score_value, missed_score_value, high_score
    caught_score_value = 0
    missed_score_value = 0
    initial_speed = 0.75
    speed_slope = .05
    eggX = [random.choice(henX) + 25]
    eggY = [henY + 40]
    egg_num = 1
    running = True
    clock = pygame.time.Clock()
    while running:
        # RGB for background
        screen.fill((100, 20, 23))
        # Background Image
        screen.blit(background, (0, 0))
        # control the speed of eggs based on caught_score_value
        for i in range(egg_num):
            eggY[i] += (initial_speed + speed_slope * caught_score_value)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # if close button is pressed it terminates
                # it is possible to tell that when that arrow is pressed terminating the program happens

                # if keystroke is pressed, check whether it is right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    basketX_change = -8
                if event.key == pygame.K_RIGHT:
                    basketX_change = 8
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYUP:  # whether we had keyborad release
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    basketX_change = 0

        #
        hen()
        for i in range(egg_num):
            egg(eggX[i], eggY[i])

        # check if the last generated egg drops enough, generate another one
        if eggY[-1] >= (henY + 150):
            # generate another egg
            egg_num += 1
            eggX.append(random.choice(henX) + 25)
            eggY.append(henY + 40)
            egg(eggX[-1], eggY[-1])


        # Check for catching the lowest egg
        if isCaught(eggX[0], eggY[0], basketX, basketY):
            # egg was caught
            # remove the first element of eggX and eggY
            eggY.pop(0)
            eggX.pop(0)
            # reduce the number of eggs by 1
            egg_num -= 1
            caught_score_value += 1
            print("number of eggs caught", caught_score_value)
            caught_egg_sound = mixer.Sound('eggcaught.mp3')
            caught_egg_sound.play()


        # if egg is low enough, it was missed
        if eggY[0] >= 540:
            if abs(basketX - eggX[0] + 8) > 32:
                # egg was missed
                missed_score_value -= 1
                print("number of eggs missed", missed_score_value)
                # Play missed_egg sound
                missed_egg_sound = mixer.Sound('eggdrop.wav')
                missed_egg_sound.play()
                # remove the first element of eggX and eggY
                eggY.pop(0)
                eggX.pop(0)
                # reduce the number of eggs by 1
                egg_num -= 1
                # show game over message
                if missed_score_value <= -10:
                    game_over()
                    pygame.display.update()
                    print(f"END of Game: Number of Collected Eggs is {caught_score_value}")
                    time.sleep(5)
                    break

            else:
                # egg was caught
                # remove the first element of eggX and eggY
                eggY.pop(0)
                eggX.pop(0)
                # reduce the number of eggs by 1
                egg_num -= 1
                caught_score_value += 1
                print("number of eggs caught", caught_score_value)
                caught_egg_sound = mixer.Sound('eggcaught.mp3')
                caught_egg_sound.play()

            # generate another egg, based on location of hens
            #eggX = random.choice(henX) + 25
            #eggY = henY + 40"""

        basketX += basketX_change
        if basketX <= 0:
            basketX = 0
        elif basketX >= 736:
            basketX = 736

        basket(basketX, basketY)


        show_scores(missed_scoreX, missed_scoreY, caught_scoreX, caught_scoreY)


        # update screen (the window game)
        pygame.display.update()
        clock.tick(60)
    if caught_score_value > high_score:
        high_score = caught_score_value
        high_score_write = open('highscore.dat', 'w')
        high_score_write.write("%s" %high_score)
        high_score_write.close()


def highscore():
    screen.fill((100, 20, 23))
    # Background Image
    screen.blit(background, (0, 0))
    h_score = start_font.render("Your Highest Score is: " + str(abs(high_score)), True, (255,127,80))
    screen.blit(h_score, (60, 80))
    over_txt_small = over_font_small.render("*Back to main menu in 5 sec", True, (10, 10, 10))
    screen.blit(over_txt_small, (220, 250))
    pygame.display.update()
    time.sleep(5)



def main_menu():
    intro = True
    menu_clock = pygame.time.Clock()
    navigation_sound = mixer.Sound('nav.wav')
    while intro:
        screen.blit(background, (0, 0))
        #pygame.display.update()
        # Adding explanation
        show_explanation()

        option1 = start_font.render("{}".format(mainmenu[0]), True, (255,165,0))
        screen.blit(option1, (50, 100))
        option2 = start_font.render("{}".format(mainmenu[1]), True, (255,165,0))
        screen.blit(option2, (50, 150))
        option3 = start_font.render("{}".format(mainmenu[2]), True, (255,165,0))
        screen.blit(option3, (50, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mainmenu[:,0] = np.roll(mainmenu[:,0],-1)
                    navigation_sound.play()
                elif event.key == pygame.K_DOWN:
                    mainmenu[:,0] = np.roll(mainmenu[:,0],1)
                    navigation_sound.play()
                elif event.key == pygame.K_RETURN:
                    navigation_sound.play()
                    if mainmenu[0, 0] == "->":
                        print("starting game")
                        game_start()
                    elif mainmenu[1, 0] == "->":
                        highscore()
                    elif mainmenu[2, 0] == "->":
                        print("Exiting")
                        intro= False
                        break
        menu_clock.tick(30)

main_menu()