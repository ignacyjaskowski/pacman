# importy

import pygame
import sys
import numpy as np
from animacja import dir,ghost,pacman
import os
from obrazy import pacman_up, pacman_down, pacman_left, pacman_right,rr,rl,rd,ru
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=256)
pygame.init()
def new_game():
    kwadrat = 40
    is_game_over = False
    plansza = np.array([['p','p','p','p','p','p','p','p','p','p','p','p','p','p','p'],
                        ['p',111,111,111,111,111,111,111,111,111,111,111,111,111,'p'],
                        ['p',111,'p','p','p','p','p',111,'p','p','p','p','p',111,'p'],
                        ['p',111,'p',111,111,111,111,111,111,111,111,111,'p',111,'p'],
                        ['p',111,'p',111,'p','p','p',111,'p','p','p',111,'p',111,'p'],
                        ['p',111,'p',111,'p','p','p',111,'p','p','p',111,'p',111,'p'],
                        ['p',111,'p',111,'p','p','p',111,'p','p','p',111,'p',111,'p'],
                        ['p',111,111,111,111,111,111,111,111,111,111,111,111,111,'p'],
                        ['p',111,'p',111,'p','p','p',111,'p','p','p',111,'p',111,'p'],
                        ['p',111,'p',111,'p','p','p',111,'p','p','p',111,'p',111,'p'],
                        ['p',111,'p',111,'p','p','p',111,'p','p','p',111,'p',111,'p'],
                        ['p',111,'p',111,111,111,111,111,111,111,111,111,'p',111,'p'],
                        ['p',111,'p','p','p','p','p',111,'p','p','p','p','p',111,'p'],
                        ['p',111,111,111,111,111,111,111,111,111,111,111,111,111,'p'],
                        ['p','p','p','p','p','p','p','p','p','p','p','p','p','p','p']])
    duch = ghost(7,7,rr,rl,rd,ru,kwadrat,plansza)
    pac_man = pacman(1,13,pacman_right,pacman_left,pacman_down,pacman_up,kwadrat,plansza,dir.left)
    return kwadrat,pac_man,is_game_over,duch,plansza
def game_over():
    global is_game_over
    w, h = screen.get_size()
    font = pygame.font.Font(None, 140)          # duży font
    text = font.render("GAME OVER", True, (255, 0, 0))
    rect = text.get_rect(center=(w//2, h//2))
    screen.blit(text, rect)
    pygame.display.flip()
    is_game_over = True
def you_win():
    global is_game_over
    w, h = screen.get_size()
    font = pygame.font.Font(None, 140)          # duży font
    text = font.render("YOU WIN!", True, (0, 255, 0))
    rect = text.get_rect(center=(w//2, h//2))
    screen.blit(text, rect)
    pygame.display.flip()
    is_game_over = True

def draw_food(y,x):
    pygame.draw.rect(screen, pink, (x * kwadrat + kwadrat//2 - kwadrat // 8, y * kwadrat + kwadrat //2 - kwadrat // 8, kwadrat//4,kwadrat//4))
def draw_p(y, x):
    pygame.draw.rect(screen, black, (x * kwadrat, y * kwadrat, kwadrat,kwadrat))
def draw():
    screen.fill(blue)
    for y in range(15):
        for x in range(15):
            if plansza[y,x] == 'p':
                draw_p(y,x)
            elif plansza[y,x] == '111':
                draw_food(y,x)
    duch.draw(screen)
    pac_man.draw(screen)
    pygame.display.flip()

snd = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..//sounds", "eating_food2.wav"))
kwadrat,pac_man,is_game_over,duch,plansza = new_game()
# stworzenie okna pygame
wysokosc = 600
szerokosc = 600
screen = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption('Pac-Man')


# Obrazek na środku
# zegar żeby program nie działał za szybko
clock = pygame.time.Clock()
fps = 60

# ustawienie kolorów
black = (0,0,0)
blue = (0,0,255)
white = (255,255,255)
pink = (255, 183, 174)

# pętla gry
running = True
while running:
    # obsługa zdarzeń
    keydown = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keydown = dir.up
            if event.key == pygame.K_RIGHT:
                keydown = dir.right
            if event.key == pygame.K_DOWN:
                keydown = dir.down
            if event.key == pygame.K_LEFT :
                keydown = dir.left
            if event.key == pygame.K_SPACE:
                kwadrat,pac_man,is_game_over,duch,plansza = new_game()
            if event.key == pygame.K_c:
                is_game_over = False
                pac_man._x = 7
                pac_man._y = 7
                pac_man.cel_y,pac_man.cel_x = pac_man.what_index(pac_man.direction)
    # logika gry
    pac_man.tick(keydown)
    if plansza[pac_man._y,pac_man._x] == '111':
        plansza[pac_man._y,pac_man._x] = '0'
        snd.play()
    duch.tick(pac_man._y,pac_man._x)
    if not is_game_over:
        draw()
    if pac_man._y == duch._y and pac_man._x == duch._x:
        game_over()
    elif '111' not in plansza:
        you_win()

    # utrzymanie fps
    clock.tick(fps)
pygame.quit()
sys.exit()
