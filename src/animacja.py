from enum import Enum
import numpy as np
class dir(Enum):
    right = "right"
    left = "left"
    stop = "stop"
    up = "up"
    down = "down"
class animacja:
    def __init__(self, items):
        self._items = list(items)
        if not self._items:
            raise ValueError("Lista nie może być pusta.")
        self._x = 0  # startowy indeks

    # jak "wypisujesz" zmienną -> dostajesz aktualny element
    def __str__(self):
        return str(self._items[self._x])


    def inc(self):
        self._x = (self._x + 1) %  len(self._items)
        return self

    # pomocnicze: aktualny element i indeks
    @property
    def value(self):
        return self._items[self._x]

    @property
    def x(self):
        return self._x
class ghost:
    def __init__(self, y,x, ar,al,ad,au, kwadrat, plansza):
        self._x = x
        self._y = y
        self.ar = ar
        self.al = al
        self.ad = ad
        self.au = au
        self.kwadrat = kwadrat
        self.how = 0
        self.what_animation = {dir.right:ar,dir.left:al,dir.down:ad,dir.up:au}
        self.odleglosci = np.zeros((15,15,15,15,2), dtype=int)
        for y in range(15):
            for x in range(15):
                if plansza[y,x] == 'p':
                    self.odleglosci[y,x] = -1
                    continue
                else:
                    self.odleglosci[y,x] = bfs(y,x,plansza)
        self.cel_y = self.odleglosci[self._y][self._x][1][13][0]
        self.cel_x = self.odleglosci[self._y][self._x][1][13][1]
        if self.cel_y < 0 or self.cel_x < 0:
            print(f"{plansza[7,7]=}")
            print(f"{y=} {x=} {self.odleglosci[y,x]=}")
            raise ValueError(f"Som ting wong: {self.cel_y=} {self.cel_x=}")
        

    def draw(self, screen):
        draw(screen,self.what_animation[self.what_direction],self.xy)
    def tick(self,cel_y,cel_x):
        self.how += 2
        if self.how == self.kwadrat:
            self.how = 0
            self._y = self.cel_y
            self._x = self.cel_x
            self.cel_y = self.odleglosci[self._y,self._x,cel_y,cel_x,0]
            self.cel_x = self.odleglosci[self._y,self._x,cel_y,cel_x,1]
    @property
    def what_direction(self):
        return what_direction(self._y,self._x,self.cel_y,self.cel_x)
    @property            
    def xy(self):
        return xy(self._y,self._x,self.cel_y,self.cel_x,self.kwadrat,self.how)
    












class pacman:
    def __init__(self, y,x, ar,al,ad,au, kwadrat, plansza,start_direction):
        self._x = x
        self._y = y
        self.ar = ar
        self.al = al
        self.ad = ad
        self.au = au
        self.old_direction = start_direction
        self.kwadrat = kwadrat
        self.how = 0
        self.swhat_animation = {dir.right:ar,dir.left:al,dir.down:ad,dir.up:au}
        self.cel_y = self.what_index(start_direction)[0]
        self.cel_x = self.what_index(start_direction)[1]
        self.direction = start_direction
        self.next_direction = start_direction
        self.plansza = plansza
        if self.cel_y < 0 or self.cel_x < 0:
            print(f"{plansza[7,7]=}")
            print(f"{y=} {x=} {self.odleglosci[y,x]=}")
            raise ValueError(f"Som ting wong: {self.cel_y=} {self.cel_x=}")
        

    def draw(self, screen):
        draw(screen,self.what_animation,self.xy)


    def tick(self,keydown):
        if keydown != None:
            self.next_direction = keydown
        if self.direction != dir.stop:
            self.how += 2
        if self.how == self.kwadrat:
            self._y = self.cel_y
            self._x = self.cel_x
            a = self.where_i_can_go
            if self.what_index(self.next_direction) in a:
                self.cel_y,self.cel_x = self.what_index(self.next_direction)
                self.direction = self.next_direction
                self.how = 0
            elif self.what_index(self.direction) in a:
                self.cel_y,self.cel_x = self.what_index(self.direction)
                self.how = 0
            elif self.direction != dir.stop:
                self.old_direction = self.direction
                self.direction = dir.stop


    def what_index(self,direction):
        return what_index(self._y,self._x,direction)
    

    @property
    def what_direction(self):
        return what_direction(self._y,self._x,self.cel_y,self.cel_x)
    

    @property            
    def xy(self):
        return xy(self._y,self._x,self.cel_y,self.cel_x,self.kwadrat,self.how)
    

    @property
    def where_i_can_go(self):
        return where_i_can_go(self._y,self._x,self.plansza)
    

    @property
    def what_animation(self):
        if self.direction == dir.stop:
            return self.swhat_animation[self.old_direction]
        return self.swhat_animation[self.direction]
    

def draw(screen,obraz,xy):
    obraz.inc()
    rect = (obraz.value).get_rect()
    rect.center = xy
    screen.blit(obraz.value, rect)


def what_direction(y,x,cel_y,cel_x):
    if y == cel_y:
        if x < cel_x:
            return dir.right
        elif x > cel_x:
            return dir.left
    elif x == cel_x:
        if y < cel_y:
            return dir.down
        elif y > cel_y:
            return dir.up
    return dir.stop
    print('blasd')
    print(f"{y=} {cel_y=} {x=} {cel_x=}")


def what_index(y,x,direction):
    if direction == dir.down:
        return (y + 1, x)
    if direction == dir.up:
        return (y - 1, x)
    if direction == dir.right:
        return (y, x + 1)
    if direction == dir.left:
        return (y, x - 1)
    if direction == dir.stop:
        return (y,x)
    

def xy(y,x,y2,x2,kwadrat,how):
    if y == y2:
        if x < x2:
            return (x * kwadrat + kwadrat // 2 + how, y * kwadrat + kwadrat // 2)
        elif x > x2:
            return (x * kwadrat + kwadrat // 2 - how,y * kwadrat + kwadrat // 2)
    elif x == x2:
        if y < y2:
            return (x * kwadrat + kwadrat // 2,y * kwadrat + kwadrat // 2 + how)
        elif y > y2:
            return (x * kwadrat + kwadrat // 2, y * kwadrat +kwadrat // 2 - how)
    return (x * kwadrat + kwadrat // 2, y * kwadrat + kwadrat // 2)
    raise RuntimeError(f"Som ting wong: {y=} {y2=} {x=} {x2=}")


def can_i_go(y,x,direction,plansza):
        y,x = what_index(y,x,direction)
        if plansza[y][x] != 'p':
            return True
        return False


def where_i_can_go(y,x,plansza):
    wynik = []
    if can_i_go(y,x,dir.up,plansza):
        wynik.append((y - 1, x))
    if can_i_go(y,x,dir.right,plansza):
        wynik.append((y, x + 1))
    if can_i_go(y,x,dir.down,plansza):
        wynik.append((y + 1, x))
    if can_i_go(y,x,dir.left,plansza):
        wynik.append((y, x - 1))
    return wynik


def bfs(y, x, plansza):
    aktualne_wierzchołki = [(y,x)]
    pszyszłe_wierzchołki = []
    wynik = np.ones((15,15,2)) * -1
    ile = 1

    while len(aktualne_wierzchołki) > 0:
        for y,x in aktualne_wierzchołki:
            w = where_i_can_go(y, x,plansza)
            for y2,x2 in w:
                if all(wynik[y2,x2] == -1):
                    pszyszłe_wierzchołki.append((y2,x2))
                    if ile == 1:
                        wynik[y2,x2] = (y2,x2)
                    elif ile > 1:
                        wynik[y2,x2] = wynik[y,x]
        aktualne_wierzchołki = pszyszłe_wierzchołki
        pszyszłe_wierzchołki = []
        ile += 1
    return wynik