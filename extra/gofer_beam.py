#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import os
import random
import sys


START, PLAY, GAMEOVER = (0, 1, 2) 
SCR_RECT = Rect(0, 0, 1000, 700)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"Gofer_Atack")
    # サウンドのロード
    Player.shot_sound = load_sound("shot.wav")
    Alien.kill_sound = load_sound("kill.wav")
    Player.bomb_sound = load_sound("bomb.wav")
    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    aliens = pygame.sprite.Group()  # エイリアングループ
    shots = pygame.sprite.Group()
    beams = pygame.sprite.Group()

    Player.containers = all
    Shot.containers = all, shots
    Alien.containers = all, aliens
    Beam.containers = all, beams
    Explosion.containers = all

    # スプライトの画像を登録
    Player.image = load_image("goAK.png")
    Shot.image = load_image("shot.png")
    Beam.image = load_image("beam.png")
    # 自機を作成
    Alien.images = split_image(load_image("alien.png"), 2)
    Explosion.images = split_image(load_image("explosion.png"), 16)

    player = Player()

    for i in range(0, 50):
        x = 600 + (i % 10) * 40
        y = 10 + (i / 10) * 40
        Alien((x,y))
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))
        all.update()
        # ミサイルとエイリアンの衝突判定
        collision_detection(player, aliens, shots, beams)
        all.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

""" def collision_detection(shots, aliens):
    衝突けんち
    # エイリアンとミサイルの衝突判定
    alien_collided = pygame.sprite.groupcollide(aliens, shots, True, True)
    for alien in alien_collided.keys():
        Alien.kill_sound.play() """

def collision_detection(player, aliens, shots, beams):
    """衝突判定"""
    # エイリアンとミサイルの衝突判定
    alien_collided = pygame.sprite.groupcollide(aliens, shots, True, True)
    for alien in alien_collided.keys():
        Alien.kill_sound.play()
        Explosion(alien.rect.center) 
    # プレイヤーとビームの衝突判定
    beam_collided = pygame.sprite.spritecollide(player, beams, True)
    if beam_collided:  # プレイヤーと衝突したビームがあれば
        Player.bomb_sound.play()
        # TODO: ゲームオーバー処理


class Player(pygame.sprite.Sprite):
    """自機"""
    speed = 10  # 移動速度
    reload_time = 5  # リロード時間
    def __init__(self):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.left  
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

class Alien(pygame.sprite.Sprite):
    """エイリアン"""
    speed = 2  # 移動速度
    animcycle = 18  # アニメーション速度
    frame = 0
    move_width = 700
    prob_beam = 0.003  # ビームを発射する確率
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.midleft = pos
        self.top = 0  # 移動できる左端
        self.bottom = self.top + self.move_width  # 移動できる右端
    def update(self):
        # 横方向への移動
        self.rect.move_ip(0,self.speed )
        if self.rect.top < self.top or self.rect.bottom > self.bottom:
            self.speed = -self.speed
        # ビームを発射
        if random.random() < self.prob_beam:
            Beam(self.rect.midleft)
        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[int(self.frame/self.animcycle%2)]

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
        if self.rect.right > SCR_RECT.right :  # 上端に達したら除去
            self.kill()

class Beam(pygame.sprite.Sprite):
    """エイリアンが発射するビーム"""
    speed = 5  # 移動速度
    def __init__(self, pos):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.move_ip( -self.speed , 0 )  # 下へ移動
        if self.rect.left < SCR_RECT.left :  # 下端に達したら除去
            self.kill()

class Explosion(pygame.sprite.Sprite):
    """爆発エフェクト"""
    animcycle = 2  # アニメーション速度
    frame = 0
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.max_frame = len(self.images) * self.animcycle  # 消滅するフレーム
        #print(self.max_frame)
    def update(self):
        # キャラクターアニメーション
        self.image = self.images[int(self.frame/self.animcycle)]
        self.frame += 1
        if self.frame == self.max_frame:
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

def split_image(image, n):
    """横に長いイメージを同じ大きさのn枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = int(w / n)
    for i in range(0, w, w1):
        surface = pygame.Surface((w1,h))
        surface.blit(image, (0,0), (i,0,w1,h))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert()
        image_list.append(surface)
    return image_list

def load_sound(filename):
    filename = os.path.join("./", filename)
    return pygame.mixer.Sound(filename)

if __name__ == "__main__":
    main()
