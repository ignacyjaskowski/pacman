import os
import pygame
import pygame.surfarray as sarr 

from animacja import animacja
folder = os.path.join(os.path.dirname(__file__), "..//obrazy")  # <-- tu wpisz swój katalog z obrazkami


def linijka(path, skala):

    
    obraz = pygame.image.load(path)
    s=pygame.Surface(obraz.get_size(), pygame.SRCALPHA)
    s.blit(obraz,(0,0))
    rgb=sarr.pixels3d(s)
    a=sarr.pixels_alpha(s)
    a[(rgb[...,0]==0)&(rgb[...,1]==0)&(rgb[...,2]==0)]=0
    del rgb,a
    nowy_rozmiar = (s.get_width() * skala, s.get_height() * skala)
    return pygame.transform.smoothscale(s, nowy_rozmiar)
    
skala = 2.5
pac1 = linijka(os.path.join(folder,"pac1.png"), skala)
pacr2 = linijka(os.path.join(folder,"pacr2.png"), skala)
pacr3 = linijka(os.path.join(folder,"pacr3.png"), skala)
pacu2 = linijka(os.path.join(folder,"pacu2.png"), skala)
pacu3 = linijka(os.path.join(folder,"pacu3.png"), skala)
pacd2 = linijka(os.path.join(folder,"pacd2.png"), skala)
pacd3 = linijka(os.path.join(folder,"pacd3.png"), skala)
pacl2 = linijka(os.path.join(folder,"pacl2.png"), skala)
pacl3 = linijka(os.path.join(folder,"pacl3.png"), skala)
rr1 = linijka(os.path.join(folder,"rr1.png"), skala)
rr2 = linijka(os.path.join(folder,"rr2.png"), skala)
rl1 = linijka(os.path.join(folder,"rl1.png"), skala)
rl2 = linijka(os.path.join(folder,"rl2.png"), skala)
rd1 = linijka(os.path.join(folder,"rd1.png"), skala)
rd2 = linijka(os.path.join(folder,"rd2.png"), skala)
ru1 = linijka(os.path.join(folder,"ru1.png"), skala)
ru2 = linijka(os.path.join(folder,"ru2.png"), skala)

rr = animacja([rr1] * 4 + [rr2] * 4)
rl = animacja([rl1] * 4 + [rl2] * 4)
rd = animacja([rd1] * 4 + [rd2] * 4)
ru = animacja([ru1] * 4 + [ru2] * 4)
pacman_up = animacja([pac1,pac1,pac1,pacu2,pacu2,pacu2,pacu3,pacu3,pacu3])
pacman_right = animacja([pac1,pac1,pac1,pacr2,pacr2,pacr2,pacr3,pacr3,pacr3])
pacman_down = animacja([pac1,pac1,pac1,pacd2,pacd2,pacd2,pacd3,pacd3,pacd3])
pacman_left = animacja([pac1,pac1,pac1,pacl2,pacl2,pacl2,pacl3,pacl3,pacl3])