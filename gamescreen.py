import main
import blocks
import sys
import time
import random
import pygame
from pygame.locals import *

#マス目を引く関数
def drawLine():
    i = 0
    j = 0
    #縦線を引く
    while i*main.BLOCK_SIZE <= main.GAME_WIDTH:
        pygame.draw.line(main.SCREEN, (0, 0, 0), (i*main.BLOCK_SIZE, 0), (i*main.BLOCK_SIZE, main.WINDOW_HEIGHT))
        i += 1
    #横線を引く
    while j*main.BLOCK_SIZE <= main.WINDOW_HEIGHT:
        pygame.draw.line(main.SCREEN, (0, 0, 0), (0, j*main.BLOCK_SIZE), (main.GAME_WIDTH, j*main.BLOCK_SIZE))
        j += 1

def drawScore(screen, score):
        font = pygame.font.SysFont(None,20)
        text = font.render("SCORE:" + str(score), False, (255,0,0))
        screen.blit(text,(200,0))
