#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import os
import sys

SCR_RECT = Rect(0, 0, 800, 600)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"Invader 02 ミサイルの発射")
    # サウンドのロード
    Player.shot_sound = load_sound("shot.wav")
    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    Player.containers = all
    Shot.containers = all
    # スプライトの画像を登録
    Player.image = load_image("goAK.png")
    Shot.image = load_image("shot.png")
    # 自機を作成
    Player()
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))
        all.update()
        all.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

class Player(pygame.sprite.Sprite):
    """自機"""
    speed = 5  # 移動速度
    reload_time = 5  # リロード時間
    def __init__(self):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.left  # プレイヤーが画面の一番下
        self.reload_timer = 0
    def update(self):
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じてプレイヤーを移動
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        self.rect.clamp_ip(SCR_RECT)
        # ミサイルの発射
        if pressed_keys[K_SPACE]:
            # リロード時間が0になるまで再発射できない
            if self.reload_timer > 0:
                # リロード中
                self.reload_timer -= 1
            else:
                # 発射！！！
                Player.shot_sound.play()
                Shot(self.rect.center)  # 作成すると同時にallに追加される
                self.reload_timer = self.reload_time

class Shot(pygame.sprite.Sprite):
    """プレイヤーが発射するミサイル"""
    speed = 10  # 移動速度
    def __init__(self, pos):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        self.rect.move_ip(self.speed, 0)  # 上へ移動
        if self.rect.right < 0:  # 上端に達したら除去
            self.kill()

def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("./", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print ("Cannot load image:", filename)
        raise SystemExit 
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def load_sound(filename):
    filename = os.path.join("./", filename)
    return pygame.mixer.Sound(filename)

if __name__ == "__main__":
    main()
