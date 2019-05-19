import sys
import time
import random
import pygame
from pygame.locals import *
import numpy as np
import blocks
import gamescreen
import map

#各定数の定義
BLOCK_SIZE = 20 #1マスの大きさ
BLOCK_COLOR = (255, 0, 0)   #ブロックの色、RGB値
BLOCK_INIT_X = 4    #ブロックの初期x
BLOCK_INIT_Y = 0    #ブロックの初期y
BLOCK_SPEED_X = 1
BLOCK_SPEED_Y = 1
MAP_HEIGHT = 20   #縦のブロック数
MAP_WIDTH = 10    #横のブロック数
MAP = map.Map(MAP_HEIGHT, MAP_WIDTH)
GAME_WIDTH = BLOCK_SIZE*MAP_WIDTH
SIDEBAR_WIDTH = 120
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH  #ウィンドウの横サイズ
WINDOW_HEIGHT = BLOCK_SIZE*MAP_HEIGHT #ウィンドウの縦サイズ
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  #ウィンドウを生成
GAMEOVER = False    #ゲームオーバーフラグ
def main():
    #初期化処理
    pygame.init()
    pygame.display.set_caption("Tetris") #タイトルを設定
    fall_cnt = 0 #落下カウント
    gr_cnt = 0 #接地秒数カウント
    score = 0
    new_block = True #新ブロック生成フラグ
    while True:
        #ブロック生成
        if new_block:
            activeBlock = blocks.Block(BLOCK_INIT_X, BLOCK_INIT_Y, random.randrange(7))
            activeBlock.draw()
            GAMEOVER = activeBlock.checkGameover(MAP)
            new_block = False
        #ゲームオーバー処理
        if GAMEOVER:
            gamescreen.drawLine()
            font = pygame.font.SysFont(None,40)
            text = font.render("GAMEOVER", False, (255,0,0))
            SCREEN.blit(text,(10,50))
            pygame.display.update()
            new_block = False
        else:
            #ブロックの移動処理
            if fall_cnt == 2:
                score += 1
                if activeBlock.fall(MAP):
                    gr_cnt += 1
                fall_cnt = 0
            fall_cnt += 1
            if pygame.key.get_pressed()[K_LEFT]:
                activeBlock.move((-1)*BLOCK_SPEED_X, MAP)
            if pygame.key.get_pressed()[K_RIGHT]:
                activeBlock.move(BLOCK_SPEED_X, MAP)
            if pygame.key.get_pressed()[K_SPACE]:
                activeBlock.rotate(MAP)
            if pygame.key.get_pressed()[K_DOWN]:
                fall_cnt = 2
            #ブロック設置判定
            if gr_cnt == 3:
                new_block = True
                MAP.embed(activeBlock)
                gr_cnt = 0

            #消失判定
            MAP.align(score)
            #描画関連
            SCREEN.fill((255,255,255))
            MAP.draw()
            activeBlock.draw()
            gamescreen.drawLine()
            gamescreen.drawScore(SCREEN, score)
            pygame.display.update()
            time.sleep(0.1)
        #pygameのイベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()   # Pygameの終了(画面閉じられる)
                sys.exit()

if __name__ == "__main__":
    main()
