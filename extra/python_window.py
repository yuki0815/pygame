#_*_coding:utf-8_*_                                                                                                                     
#ウィンドウを表示する                                                                                                                   
import sys
import pygame
from pygame.locals import *

pygame.init() #pygameの初期化                                                                                                           
screen = pygame.display.set_mode((400, 300)) #ウィンドウの大きさ                                                                       
pygame.display.set_caption("PyGame") #タイトルバー                                                                                      

# mainループ                                                                                                                            
def main():
    while True:
        screen.fill((0,0,0)) #ウィンドウの背景色                                          
        #イベントの取得
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() #閉じるボタンが押されたらプログラムを終了                                                                 
                sys.exit
        pygame.display.update()

if __name__ == '__main__':
    main()