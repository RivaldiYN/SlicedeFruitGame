import pygame
from pygame import mixer
import os, sys
import random
from abc import ABC, abstractmethod

# inisialisasi pygame dan buat papan game 
WIDTH = 800
HEIGHT = 500                    
FPS = 9.5                                               
pygame.init()                                            #mengontrol seberapa sering tampilan game harus direfresh. Dalam kasus kami, ini akan direfresh setiap 9.5 per detik
pygame.display.set_caption('Slice de Fruit')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   #setting ukuran tampilan game
clock = pygame.time.Clock()
# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Struktur umum dari method buah
class generate_acak_buah():
    def __init__(self):
        self.data = {}

    def generate_buah(self, fruit):
        self.fruit_path = "images/" + fruit
        self.data[fruit] = {
            'img': pygame.image.load(self.fruit_path),
            'x' : random.randint(100,500),          #kondisi di mana buah harus diposisikan pada koordinat x
            'y' : 800,
            'speed_x': random.randint(-10,10),      #seberapa cepat buah harus bergerak dalam arah x. Mengontrol pergerakan buah secara diagonal
            'speed_y': random.randint(-80, -60),    #mengontrol kecepatan buah di y-directionn ( UP )
            'throw': False,                         #menentukan apakah koordinat buah yang dihasilkan berada di luar tampilan permainan atau tidak. Jika di luar, maka akan dibuang
            't': 0,                                 
            'hit': False,
        }

        if random.random() >= 0.75:     #Mengembalikan angka floating point acak berikutnya dalam rentang [0.0, 1.0) untuk menyimpan buah di dalam gameDisplay
            self.data[fruit]['throw'] = True
        else:
            self.data[fruit]['throw'] = False

# Array untuk menyimpan data generasi buah acak

class GameObject(ABC):
    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img_path)

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def draw():
        pass

class main(generate_acak_buah, GameObject):
    def __init__(self):
        self.player_lives = 3                                                #jumlah nyawa pemain
        self.score = 0                                                       #set score dari 0
        self.fruits = ['melon.png', 'orange.png', 'pomegranate.png', 'guava.png', 'bomb.png']    #entitas yang ada pada game

    def update(self, x, y, g, t):
        if self.throw:
            self.x = x
            self.y = y
            self.speed_y += g*self.t
            self.t = t + 1

    def draw(self, screen):
        if self.y <= 800:
            screen.blit(self.img, (self.x, self.y))

# Music
class music():
    def __init__(self):
        self.bgm = "audio/music_bg.wav"
        self.die = "audio/die.wav"
        self.hit = "audio/hit.wav"
        self.point = "audio/knife-slice-41231.wav"

play_music = music()
main_1 = main()

background = pygame.image.load('back.jpg')                                  #game background
font = pygame.font.Font(os.path.join(os.getcwd(), 'dragonfont.otf'), 42)
score_text = font.render('Score : ' + str(main_1.score), True, (255, 255, 255))    #tampilan score
lives_icon = pygame.image.load('images/white_lives.png')                    #gambar untuk tampilin nyawa



fruit_1 = generate_acak_buah()
for a in range (len(main_1.fruits)):
    fruit_1.generate_buah(main_1.fruits[a])

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

# Pendefinisian font di layar
font_name = pygame.font.match_font('dragonfont.otf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

# Setting nyawa pemain
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #mendapatkan koordinat (x,y) dari ikon nyawa (berada di sisi paling kanan atas)
        img_rect.x = int(x + 35 * i)    #mengatur ikon nyawa berikutnya 35 piksel dari yang sebelumnya
        img_rect.y = y                  #mengatur berapa banyak piksel ikon nyawa harus diposisikan dari atas layar
        display.blit(img, img_rect)

# Tampilan untuk gameover & tampilan depan game
class tampil_gameover(main):
    def __init__(self):
        gameDisplay.blit(background, (0,0))
        draw_text(gameDisplay, "SLICE de FRUIT!", 90, WIDTH / 2, HEIGHT / 4)
        if not game_over :
            draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)

        draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    mixer.music.load(play_music.bgm)
                    mixer.music.play(-1)
                    waiting = False

# Game Loop
first_round = True
game_over = True        #mengakhiri permainan While loop jika lebih dari 3-Bom dipotong
game_running = True     #digunakan untuk mengelola loop game

while game_running :
    if game_over :
        if first_round :
            tampil_gameover()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():
        # kondisi untuk memeriksa menutup jendela
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    for key, value in fruit_1.data.items():
        if value['throw']:
            value['x'] += value['speed_x']          #memindahkan buah dalam koordinat x
            value['y'] += value['speed_y']          #memindahkan buah dalam koordinat y
            value['speed_y'] += (1 * value['t'])    #meningkatkan y-kordinat
            value['t'] += 1                         #meningkatkan speed_y untuk loop berikutnya

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #menampilkan buah di dalam layar secara dinamis
            else:
                fruit_1.generate_buah(key)

            current_position = pygame.mouse.get_pos()   #mendapatkan koordinat saat ini (x, y) dalam piksel mouse

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                if key == 'bomb.png':
                    hit = mixer.Sound(play_music.hit)
                    hit.play()
                    player_lives -= 1
                    if player_lives == 0:
                        
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)
                    #kondisi di mana pengguna mengklik bom sebanyak tiga kali, tampilan GAME OVER harus ditampilkan dan jendela harus disetel ulang
                    if player_lives < 1 :
                        die_sound = mixer.Sound(play_music.die)
                        die_sound.play()
                        mixer.music.stop()
                        tampil_gameover()
                        game_over = True
                        pygame.display.update()

                        #backsound gameover
                    half_fruit_path = "images/half_bomb.png"
                else:
                    half_fruit_path = "images/" + "half_" + key

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    point_sound = mixer.Sound(play_music.point)
                    point_sound.play()
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True

        else:
            fruit_1.generate_buah(key)
            
    pygame.display.update()
    clock.tick(FPS)      # tetap jalankan loop pada kecepatan yang tepat (mengelola frame/detik. Loop harus diperbarui setelah setiap 9.5 per detik
                        

pygame.quit()