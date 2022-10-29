import pygame
import sys
from button import Button
from slide import *
from pygame import mixer as pg
import main

pg.init()

pygame.init()

SCREEN = pygame.display.set_mode((840, 680))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets\imgs\Background.png")

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets\\fonts\\HKGrotesk-Regular.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu_o()

        pygame.display.update()

def paused():
    pygame.mixer.music.pause()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def main_menu_o():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("||--|- OPTIONS -|-||", True, "#29d250")
        MENU_RECT = MENU_TEXT.get_rect(center=(410, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets\imgs\play_back.png"), pos=(420, 250),
                             text_input="MUSIC OFF", font=get_font(20), base_color="#000000", hovering_color="White")
        SHUFFLE_BUTTON = Button(image=pygame.image.load("assets\imgs\opt_back.png"), pos=(420, 300),
                                text_input="CHANGE MUSIC", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets\imgs\quit_back.png"), pos=(420, 480),
                             text_input="BACK", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SHUFFLE_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    paused()

                elif SHUFFLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shuffle_music(music_list)

                elif BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main.main_menu()

        pygame.display.update()

main_menu_o()
