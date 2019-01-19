#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import os
import random
import sys


START, PLAY, GAMEOVER = (0, 1, 2)
SCR_RECT = Rect(0, 0, 1000, 700)

class Gopher:
    game_state = START
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Gofer_Atack")
        #素材の読み込み
        self.load_images()
        self.load_sounds()
        #ゲームの初期化
        self.init_game()
        #メイン処理
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self):
        # ゲーム状態
        #self.game_state = START
        # スプライトグループを作成して登録
        self.all = pygame.sprite.RenderUpdates()
        self.aliens = pygame.sprite.Group()  # エイリアングループ
        self.shots = pygame.sprite.Group()
        self.beams = pygame.sprite.Group()

        Player.containers = self.all,
        Shot.containers = self.all, self.shots
        Alien.containers = self.all, self.aliens
        Beam.containers = self.all,self.beams
        Explosion.containers = self.all
        PlayerExplosion.containers = self.all
        # 自機を作成
        self.player = Player()
        #敵キャラの作成
        for i in range(0, 50):
            x = 600 + (i % 10) * 40
            y = 10 + (i / 10) * 40
            Alien((x,y))

    def update(self):
        """ゲーム状態の更新"""
        if Gopher.game_state == PLAY:
            self.all.update()
            # ミサイルとエイリアンの衝突判定
            self.collision_detection()
            # エイリアンをすべて倒したらゲームオーバー
            if len(self.aliens.sprites()) == 0:
                Gopher.game_state = GAMEOVER

    def draw(self, screen):
        """描画"""
        screen.fill((0, 0, 0))
        if Gopher.game_state == START:  # スタート画面
            # タイトルを描画
            title_font = pygame.font.SysFont(None, 80)
            title = title_font.render("Gopher is DIE !!", False, (255,0,0))
            screen.blit(title, ((SCR_RECT.width-title.get_width())/2, 100))
            # エイリアンを描画
            alien_image = Player.image
            screen.blit(alien_image, ((SCR_RECT.width-alien_image.get_width())/2, 200))
            # PUSH STARTを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255,255,255))
            screen.blit(push_space, ((SCR_RECT.width-push_space.get_width())/2, 400))
            # クレジットを描画
            credit_font = pygame.font.SysFont(None, 20)
            credit = credit_font.render(u"made by FI Yuki Okuno", False, (255,255,255))
            screen.blit(credit, ((SCR_RECT.width-credit.get_width())/2, 500))
        elif Gopher.game_state == PLAY:  # ゲームプレイ画面
            self.all.draw(screen)
        elif Gopher.game_state == GAMEOVER:  # ゲームオーバー画面
            # GAME OVERを描画
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("Gopher is DIED....", False, (255,0,0))
            screen.blit(gameover, ((SCR_RECT.width-gameover.get_width())/2, 100))
            # エイリアンを描画
            alien_image = Alien.images[0]
            screen.blit(alien_image, ((SCR_RECT.width-alien_image.get_width())/2, 200))
            # PUSH STARTを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255,255,255))
            screen.blit(push_space, ((SCR_RECT.width-push_space.get_width())/2, 400))

            made_font = pygame.font.SysFont(None, 30)
            made_space = made_font.render("This game is created in python !!", False, (255,255,255))
            screen.blit(made_space, ((SCR_RECT.width-made_space.get_width())/2, 500))

    def key_handler(self):
        """キーハンドラー"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if Gopher.game_state == START:  # スタート画面でスペースを押したとき
                    Gopher.game_state = PLAY
                elif Gopher.game_state == GAMEOVER:  # ゲームオーバー画面でスペースを押したとき
                    self.init_game()
                    # ゲームを初期化して再開
                    Gopher.game_state = START

    def collision_detection(self):
        """衝突判定"""
    # エイリアンとミサイルの衝突判定
        alien_collided = pygame.sprite.groupcollide(self.aliens, self.shots, True, True)
        for alien in alien_collided.keys():
            Alien.kill_sound.play()
            Explosion(alien.rect.center) 
        # プレイヤーとビームの衝突判定
        beam_collided = pygame.sprite.spritecollide(self.player, self.beams, True)
        if beam_collided:
            Player.bomb_sound.play()
            PlayerExplosion(self.player.rect.center)

    def load_images(self):
        # スプライトの画像を登録
        Player.image = PlayerExplosion.image = load_image("goAK.png")
        Shot.image = load_image("shot.png")
        Beam.image = load_image("beam.png")
        Alien.images = split_image(load_image("alien.png"), 2)
        Explosion.images = split_image(load_image("explosion.png"), 16)
        PlayerExplosion.images = split_image(load_image("go_Ex.png"), 16)

    def load_sounds(self):
        # サウンドのロード
        Player.shot_sound = load_sound("shot.wav")
        Alien.kill_sound = load_sound("kill.wav")
        Player.bomb_sound = load_sound("bomb.wav")

    def set_state() :
        #print(type(self.game_state))
        Gopher.game_state = GAMEOVER
        #self.game_state = GAMEOVER


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
    animcycle = 6  # アニメーション速度
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

class PlayerExplosion(pygame.sprite.Sprite):
    """爆発エフェクト"""
    animcycle = 10 # アニメーション速度
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
            Gopher.set_state()#= GAMEOVER

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
    Gopher()
