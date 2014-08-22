'''
  _____  _                                  __  __       _ _       
 |  __ \| |                                |  \/  |     | (_)      
 | |  | | |__   __ _ _ __ ___   __ _ _ __  | \  / |_   _| |_  __ _ 
 | |  | | '_ \ / _` | '_ ` _ \ / _` | '__| | |\/| | | | | | |/ _` |
 | |__| | | | | (_| | | | | | | (_| | |    | |  | | |_| | | | (_| |
 |_____/|_| |_|\__,_|_| |_| |_|\__,_|_|    |_|  |_|\__,_|_|_|\__,_|

'''



import curses
from curses import  KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint


WIDTH = 120
HEIGHT = 30
MAX_X = WIDTH-2
MAX_Y = HEIGHT-2
SNAKE_LENGTH = 5
SNAKE_X = SNAKE_LENGTH + 1
SNAKE_Y = 3
TIMEOUT = 100



class Snake(object):
    REV_DIR_MAP = {
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
    }
    
    def __init__(self, x, y, window):
        self.body_list = []
        self.hit_score = 0
        self.timeout = TIMEOUT
        # buat dua body snake
        for i in range(SNAKE_LENGTH, 0, -1):
            self.body_list.append(Body(x - i, y))
        # buat kepala snake
        self.body_list.append(Body(x, y, '@'))
        self.window = window
        self.direction = KEY_RIGHT
        self.last_head_coor = (x, y)
        self.direction_map = {
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
        }
        
    @property
    def score(self):
        return 'Score : {}'.format(self.hit_score)
        
    def add_body(self, body_list):
        self.body_list.extend(body_list)
    
    def eat_food(self,food):
        food.reset()
        body = Body(self.last_head_coor[0], self.last_head_coor[1])
        self.body_list.insert(-1, body)
        self.hit_score += 1
        if self.hit_score % 3 == 0:
            self.timeout -= 5
            self.window.timeout(self.timeout)
        
    @property    
    def nabrak(self):
        return any([ body.coor == self.kepala.coor for body in self.body_list[:-1] ])
    
    def update(self):
        #merubah posisi body snake dengan body yg didepannya, dimulai dari belakang
        for idx, body in enumerate(self.body_list[:-1]):
            body.x = self.body_list[idx+1].x
            body.y = self.body_list[idx+1].y
            
        self.last_head_coor = (self.kepala.x,self.kepala.y)
        self.direction_map[self.direction]()
    
    def change_direction(self, direction):
        if direction != Snake.REV_DIR_MAP[self.direction]:
            self.direction = direction
    
    def render(self):
        for body in self.body_list:
            self.window.addstr(body.y, body.x, body.char)
    
    @property        
    def kepala(self):
        return self.body_list[-1]
        
    @property        
    def coor(self):
        return self.kepala.x, self.kepala.y
        
    def move_up(self):
        self.kepala.y -= 1
        if self.kepala.y < 1:
            self.kepala.y = MAX_Y
            
    def move_down(self):
        self.kepala.y += 1
        if self.kepala.y > MAX_Y:
            self.kepala.y = 1
    
    def move_left(self):
        self.kepala.x -= 1
        if self.kepala.x < 1:
            self.kepala.x = MAX_X
            
    def move_right(self):
        self.kepala.x += 1
        if self.kepala.x > MAX_X:
            self.kepala.x = 1
    

class Body(object):
    def __init__(self, x, y, char='#'):
        self.x = x
        self.y = y
        self.char = char
        
    @property
    def coor(self):
        return self.x, self.y
        
            
            
            
class Food(object):
    def __init__(self, window, char='*'):
        self.x = randint(1,MAX_X)
        self.y = randint(1,MAX_Y)
        self.char = char
        self.window = window
        
    def render(self):
        self.window.addstr(self.y, self.x, self.char)
        
    def reset(self):
        self.x = randint(1,MAX_X)
        self.y = randint(1,MAX_Y)
        
        

if __name__ == '__main__':
	curses.initscr()
	window = curses.newwin(HEIGHT, WIDTH, 0, 0) 
	window.timeout(TIMEOUT)
	window.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	window.border(0)

	snake = Snake(SNAKE_X, SNAKE_Y, window)
	food = Food(window, 'A')

	while True:
		window.clear()
		window.border(0)
		snake.render()
		food.render()
		window.addstr(0, 5, snake.score)
		event = window.getch()
		
		if event == 27:
			break
			
		if event in [ KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT ]:
			snake.change_direction(event)
		
		if snake.kepala.x == food.x and snake.kepala.y == food.y:
			snake.eat_food(food)
			
		if event == 32:
			key = -1
			while key != 32:
				key = window.getch()
		
		snake.update()
		if snake.nabrak:
			break
			
	curses.endwin()

