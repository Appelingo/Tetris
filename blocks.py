import sys
import time
import random
import pygame
from pygame.locals import *
import numpy as np
import main
import blocks
T = np.array([[1, 1, 1],
              [0, 1, 0]])

I = np.array([[2],
              [2],
              [2],
              [2]])

S = np.array([[3, 3],
              [3, 3]])

L1 = np.array([[0, 0, 4],
               [4, 4, 4]])

L2 = np.array([[5, 0, 0],
               [5, 5, 5]])

Z1 = np.array([[6, 6, 0],
               [0, 6, 6]])

Z2 = np.array([[0, 7, 7],
               [7, 7, 0]])

#ランダム抽出用のリスト
SHAPE_LIST = [T, I, S, L1, L2, Z1, Z2]
COLOR_LIST = [(255,0,0), (0,255,0), (0,0,255), (255,0,255),
               (128,128,0), (0,255,255),(0,0,0)]
class Block:
    def __init__(self, initX, initY, inittype):
        self.x = initX
        self.y = initY
        self.type = inittype
        self.shape = SHAPE_LIST[inittype]
        self.color = COLOR_LIST[inittype]

    def draw(self):
        #x,yを左上として(y行目のj列目を基準として)ブロックを描画
        i = 0
        for line in self.shape:
            j = 0
            for cel in line:
                if cel > 0:
                    pygame.draw.rect(main.SCREEN, COLOR_LIST[self.type], pygame.Rect(((self.x + j)*main.BLOCK_SIZE , (self.y + i)*main.BLOCK_SIZE), (main.BLOCK_SIZE, main.BLOCK_SIZE)))
                j += 1
            i += 1
        pass

    def fall(self, map):
        under = False
        nozeros = np.nonzero(self.shape)
        i = 0
        #下がマップの底かどうか判定
        if self.y + len(self.shape) + 1> main.MAP_HEIGHT:
            under = True
        #下が底じゃないときには下にブロックがあるか判定
        else:
            while i < len(nozeros[0]):
                if map.field[self.y + nozeros[0][i] + 1][self.x + nozeros[1][i]] > 0:
                    under = True
                i += 1
        #下に何もなければ落下処理
        if not under:
            self.y += 1
        return under
        pass

    def move(self, speed, map):
        side = False
        if speed < 0:
            if self.x + speed< 0:
                print("KABE0")
                side = True
            else:
                i = 0
                while i < len(self.shape):
                    if self.shape[i][0] > 0 and map.field[self.y + i][self.x + speed] > 0:
                        side = True
                    i += 1
        elif self.x + len(self.shape[0]) + 1> main.MAP_WIDTH:
            print("KABE10")
            side = True
        else:
            i = 0
            while i < len(self.shape):
                if self.shape[i][len(self.shape[0]) - 1] > 0 and map.field[self.y + i][self.x + len(self.shape[0]) - 1 + speed] > 0:
                    side = True
                i += 1

        if not side:
            self.x += speed
        return side

    def rotate(self, map):
        rotation = np.zeros((len(self.shape[0]), len(self.shape)))
        i = len(self.shape) - 1
        for line in self.shape:
            j = 0
            for column in line:
                rotation[j, i] = column
                j += 1
            i -= 1
        rotatable = True
        k = 0
        for line in rotation:
            l = 0
            for cel in line:
                if cel and self.x + l <main.MAP_WIDTH:
                    if map.field[self.y + k][self.x + l]:
                        rotatable = False
                l += 1
            k += 1
        if rotatable:
            self.shape = rotation
            if self.y + len(self.shape) > main.MAP_HEIGHT:
                self.y = main.MAP_HEIGHT - len(self.shape)
            if self.x + len(self.shape[0]) > main.MAP_WIDTH:
                self.x = main.MAP_WIDTH - len(self.shape[0])
    def checkGameover(self, map):
        OVER = False
        i = 0
        for line in self.shape:
            j = 0
            for cel in line:
                if cel and map.field[self.y + i][self.x + j]:
                    OVER = True
        return OVER
