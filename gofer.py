# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

def main():
    pygame.init() # 初期化
    screen = pygame.display.set_mode((800, 600)) # ウィンドウサイズの指定
    pygame.display.set_caption("yatte_mita") # ウィンドウの上の方に出てくるアレの指定
    bg = pygame.image.load("gofer.jpg").convert_alpha() # 背景画像の指定
    rect_bg = bg.get_rect() # 画像のサイズ取得？？だと思われる
    font = pygame.font.Font(None, 100) 

    while(True):
        screen.fill((255, 0, 255)) # 背景色の指定。RGBのはず
        screen.blit(bg, rect_bg) # 背景画像の描画
        text = font.render("Oh my GOD !!", True, (0, 0, 0)) # 追加コード：テキスト内容と色（ここでは黒）の設定
        screen.blit(text, [200, 300]) 
        #pygame.time.wait(30) # 更新間隔。多分ミリ秒
        pygame.display.update() # 画面更新

        for event in pygame.event.get(): # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()