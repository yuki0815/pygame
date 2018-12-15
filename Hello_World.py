# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("test")
    font = pygame.font.Font(None, 50)                        # 追加コード：フォントとサイズの設定

    while (1):
        screen.fill((255, 255, 255))
        text = font.render("Oh my GOD !!", True, (0, 0, 0)) # 追加コード：テキスト内容と色（ここでは黒）の設定
        screen.blit(text, [200, 300])                        # 追加コード：表示するテキストと表示位置の設定
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()