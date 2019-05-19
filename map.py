import sys
import time
import random
import pygame
import copy
from pygame.locals import *
import numpy as np
import blocks
import gamescreen
import main


class Map:
    def __init__(self, height, width):
        self.field = np.zeros((height, width), dtype=np.int64)  #height行width列の0行列を作成


    def embed(self, block):
        #blockのx,yを基準に非ゼロ要素をfieldに代入していく
        nozeros = np.nonzero(block.shape)    #非ゼロ要素のインデックスを取得
        k = 0
        while k < len(nozeros[0]):
            self.field[block.y + nozeros[0][k]][block.x + nozeros[1][k]] = block.shape[nozeros[0][k]][nozeros[1][k]]
            k += 1

    def draw(self):
        #fieldの全マスを見て、入ってる数字に応じて色塗り
        nozeros = np.nonzero(self.field)
        i = 0
        while i < len(nozeros[0]):
            pygame.draw.rect(main.SCREEN, blocks.COLOR_LIST[self.field[nozeros[0][i]][nozeros[1][i]] - 1], pygame.Rect((nozeros[1][i]*main.BLOCK_SIZE, nozeros[0][i]*main.BLOCK_SIZE), (main.BLOCK_SIZE, main.BLOCK_SIZE)))
            i += 1

    def align(self,score):
        i = 0
        for line in self.field:
            if all(line):
                score += 10
                cp = copy.deepcopy(self.field[0:i,:])
                self.field[0] = np.zeros_like(self.field[0])
                j = 1
                for cp_line in cp:
                    self.field[j] = copy.deepcopy(cp_line)
                    j += 1
            i += 1

    def deb_draw(self):
        i = 0
        for line in self.field:
            j = 0
            for cel in line:
                font = pygame.font.SysFont(None, 30)
                value = font.render(str(cel), False, (0,0,0))
                main.SCREEN.blit(value, (j*main.BLOCK_SIZE,i*main.BLOCK_SIZE))
                j += 1
            i += 1
