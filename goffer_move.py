#_*_coding:utf-8_*_
#キー操作する
import sys
import pygame
from pygame.locals import *

pygame.init() #pygameの初期化
screen = pygame.display.set_mode((800, 600))  #ウィンドウの大きさ
pygame.display.set_caption("PyGame")  #タイトルバー
image = pygame.image.load("./gogogo.jpg")  #画像を読み込む

pygame.key.set_repeat(5,5)  #キーの押下と押しっぱなしの取得(追加したとこ)
position = [400, 300] #座標を配列に[x座標, y座標](追加したとこ)

#mainループ
def main() :
    while True:
        screen.fill((255,0,255))  #ウィンドウの背景色

        #イベントの取得
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()  #閉じるボタンが押されたらプログラムを終了
                sys.exit

            #キー操作(追加したとこ)
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    position[0] -= 5
                elif event.key == K_RIGHT:
                    position[0] += 5
                elif event.key == K_UP:
                    position[1] -= 5
                elif event.key == K_DOWN:
                    position[1] += 5

        #画面の端に行ったら反対から出るようにする(追加したとこ)
        position[0] = position[0] % 800
        position[1] = position[1] % 600

        #画像の描画位置(追加したとこ)
        rect = image.get_rect()
        rect.center = position

        #画像の描画
        screen.blit(image, rect)
        pygame.display.update()

if __name__ == '__main__':
    main()