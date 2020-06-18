from pygame import *
from random import randint

STATE = 'in menu' # 'in menu', 'in game over', 'in game', 'in pause'
BEST_RESULT = 0
NOW_RESULT = 0
GREEN = (0, 255, 0)
PINK = (255, 100, 150)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
FPS = 20
class Button():
    def __init__(self, x, y, name):
        self.image = Surface((80, 30))
        self.image.fill(GRAY)
        f = font.Font(None, 15)
        text = f.render(name, 1, BLACK)
        place = text.get_rect(center=(40, 15))
        self.image.blit(text, (place[0], place[1]))
        self.xy = (x-40, y-15)
    def pressed(self, pos):
        return self.xy[0]<pos[0] and pos[0]<self.xy[0]+80 and self.xy[1]<pos[1] and pos[1]<self.xy[1]+30

class Snake():
    def __init__(self):
        self.image = Surface((6, 6))
        self.image.fill(GREEN)
        draw.circle(self.image, PINK, (3, 3), 3)
        self.head = Surface((6, 6))
        self.head.fill(GREEN)
        draw.circle(self.head, RED, (3, 3), 3)
        self.koord = [[15, 15], [15, 16]]
        self.dlina = 2
        self.napr = 'd'
    def go(self):
        x = list(self.koord[-1])
        if self.napr == 'u':
            x[1] -= 1
        elif self.napr == 'd':
            x[1] += 1
        elif self.napr == 'r':
            x[0] += 1
        else:
            x[0] -= 1
        self.koord.append(x)
        if len(self.koord) > self.dlina:
            self.koord.pop(0)
        self.test_going()
    def test_going(self):
        global STATE
        x = self.koord[-1]
        if x[0] < 0 or x[0] > 149 or x[1] < 0 or x[1] > 149 or x in self.koord[:len(self.koord)-1:]:
            STATE = 'in game over'
    def test_on_apple(self, apples):
        for s in self.koord:
            i = 0
            while i < len(apples):
                if apples[i] == s:
                    global NOW_RESULT
                    NOW_RESULT += 10
                    self.dlina += 1
                    apples.pop(i)
                i+=1

class Apples():
    def __init__(self):
        self.image = Surface((6, 6))
        self.image.fill(GREEN)
        draw.circle(self.image, YELLOW, (3, 3), 3)
        self.koord = []
    def add_apple(self, x, y):
        self.koord.append((x, y))

init()
sc = display.set_mode((900, 900))
window = Surface((900, 900))
grass = Surface((6, 6))
grass.fill(GREEN)
snake = Snake()
apples = Apples()
clock = time.Clock()
but_to_menu = Button(50, 150, 'MENU')
but_to_pause = Button(850, 150, 'PAUSE')
but_continue = Button(450, 450, 'CONTINUE')
but_enter = Button(450, 450, 'START GAME')
but_exit = Button(50, 450, 'EXIT')
while 1:
    clock.tick(FPS)

    for ev in event.get():
        if ev.type == QUIT:
            quit()
    
    keys = key.get_pressed()
    if keys[K_LEFT] and STATE == 'in game':
        snake.napr = 'l'
    elif keys[K_RIGHT] and STATE == 'in game':
        snake.napr = 'r'
    elif keys[K_UP] and STATE == 'in game':
        snake.napr = 'u'
    elif keys[K_DOWN] and STATE == 'in game':
        snake.napr = 'd'

    mouses = mouse.get_pressed()
    if mouses[0]:
        pos = mouse.get_pos()
        if STATE == 'in game' and but_to_pause.pressed(pos):
            STATE = 'in pause'
        elif STATE == 'in pause' and but_continue.pressed(pos):
            STATE = 'in game'
        elif (STATE == 'in pause' or STATE == 'in game') and but_to_menu.pressed(pos):
            STATE = 'in game over'
        elif STATE == 'in game over' and but_to_menu.pressed(pos):
            BEST_RESULT = max(BEST_RESULT, NOW_RESULT)
            STATE = 'in menu'
        elif STATE == 'in menu' and but_enter.pressed(pos):
            STATE = 'in game'
            snake = Snake()
            NOW_RESULT = 0
        elif STATE == 'in menu' and but_exit.pressed(pos):
            quit()
    
    if STATE == 'in game':
        if not randint(0, 5) and len(apples.koord) < 50:
            x = randint(0, 149)
            y = randint(0, 149)
            if not [x, y] in snake.koord:
                apples.koord.append([x, y])

        snake.test_on_apple(apples.koord)
        snake.go()

    window.fill(WHITE)
    if STATE == 'in game' or STATE == 'in pause' or STATE == 'in game over':
        for i in range(150):
            for j in range(150):
                if [i, j] == snake.koord[-1]:
                    window.blit(snake.head, (i*6, (j+1)*6))
                elif [i, j] in snake.koord:
                    window.blit(snake.image, (i*6, (j+1)*6))
                elif [i, j] in apples.koord:
                    window.blit(apples.image, (i*6, (j+1)*6))
                else:
                    window.blit(grass, (i*6, (j+1)*6))
        window.blit(but_to_menu.image, but_to_menu.xy)
        if STATE == 'in game':
            f = font.Font(None, 18)
            text = f.render('SCORE: '+str(NOW_RESULT), 1, BLACK)
            window.blit(text, (50, 50))
            window.blit(but_to_pause.image, but_to_pause.xy)
        elif STATE == 'in pause':
            f = font.Font(None, 18)
            text = f.render('SCORE: '+str(NOW_RESULT), 1, BLACK)
            window.blit(text, (50, 50))
            window.blit(but_continue.image, but_continue.xy)
        else:
            f = font.Font(None, 48)
            text = f.render('GAME OVER', 1, BLACK)
            window.blit(text, (400, 350))
            text = f.render('SCORE: '+str(NOW_RESULT), 1, BLACK)
            window.blit(text, (400, 450))
            text = f.render('BEST SCORE: '+str(max(NOW_RESULT, BEST_RESULT)), 1, BLACK)
            window.blit(text, (400, 550))
    else:
        window.blit(but_enter.image, but_enter.xy)
        window.blit(but_exit.image, but_exit.xy)
    sc.blit(window, (0, 0))
    display.update()
