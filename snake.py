import curses, time, random
from sound import Sound

UP, RIGHT, DOWN, LEFT = range(4)
FREE_SPACE, SNAKE_DOT, FOOD, WALL, GHOST = range(5)
AVAILABLE_FOOD = ('\U0001F346','\U0001F352','\U0001F34C','\U0001F351') # ("🍆","🍒","🍌","🍑")

MAP_SIZE = 30 # Defines map area
VELOCITY = 10 # Set intended FPS here...

TOTAL_GHOST_FRAMES = VELOCITY * 5
TOTAL_NEW_GHOST_FRAMES = VELOCITY * 18

SOUNDS = (Sound.play_walking_sound, Sound.play_eating_sound, Sound.play_ghost_sound, Sound.play_death_sound)

class SnakeDot:
    def __init__(self, x, y, lifetime):
        self.x = x
        self.y = y
        self.lifetime = lifetime
    
    def decrease_lifetime(self):
        self.lifetime -= 1
        return True if self.lifetime == 0 else False
    
class Ghost:
    def __init__(self,location):
        self.location = location
        self.frames = 0


class Map:
    def __init__(self):
        self.size = MAP_SIZE
        self.score = 0
        self.map = [[FREE_SPACE] * self.size for _ in range(self.size)]
        self.snake_dots = []
        self.ghosts = []
        self.new_ghost_frames = 0

        for i in range(self.size):
            self.map[i][0] = WALL
            self.map[0][i] = WALL
            self.map[self.size-1][i] = WALL
            self.map[i][self.size-1] = WALL

        self.ghosts.append(Ghost((0,0)))
        self.set_food_location()

    def add_new_ghost(self):
        if(self.new_ghost_frames == TOTAL_NEW_GHOST_FRAMES):
            self.ghosts.append(Ghost((0,0)))
            self.new_ghost_frames=0
        else:
            self.new_ghost_frames+=1

    def get_free_space(self, space_type):
        condition = lambda x,y: self.map[y][x] == FREE_SPACE and \
        (((x < x_cur-random.randint(0,2) or x > x_cur+random.randint(0,2)) and (y < y_cur-random.randint(0,2) or y > y_cur+random.randint(0,2))) or \
        self.score > 100)

        while(True):
            x = random.randint(1, self.size - 3)
            y = random.randint(1, self.size - 3)
            if(space_type == GHOST):
                x = x-((x-x_cur)//2)
                y = y-((y-y_cur)//2)
            if(condition(x,y)):
                return (x,y)
            else:
                continue

    def set_food_location(self):
        global current_food
        current_food = get_random_fruit()
        x,y = self.get_free_space(FOOD)
        self.map[y][x] = FOOD

    def set_ghost_location(self):
        for ghost in self.ghosts:
            if(ghost.frames - random.randint(0,5) >= TOTAL_GHOST_FRAMES):
                if(ghost.location != (0,0)):
                    self.map[ghost.location[1]][ghost.location[0]] = FREE_SPACE
                    ghost.location = (0,0)
                random_number = random.randint(0, int(self.size**random.randint(1,2)*0.75))
                if(random_number < self.score):
                    ghost.location = self.get_free_space(GHOST)
                    SOUNDS[2]()
                    self.map[ghost.location[1]][ghost.location[0]] = GHOST
                ghost.frames = 0
            else:
                ghost.frames += 1

    def set_snake_location(self, x, y):
        if(self.map[y][x] == FREE_SPACE):
            self.map[y][x] = SNAKE_DOT
            self.snake_dots.append(SnakeDot(x,y,3+self.score))
            SOUNDS[0]()
            return True
        elif(self.map[y][x] == FOOD):
            self.score+=1
            self.map[y][x] = SNAKE_DOT
            self.set_food_location()
            self.snake_dots.append(SnakeDot(x,y,3+self.score))
            SOUNDS[1]()
            return True
        elif(self.map[y][x] == SNAKE_DOT or self.map[y][x] == WALL or self.map[y][x] == GHOST):
            SOUNDS[3]()
            return False
        
    def print_map(self):
        global current_food
        screen.move(screen.getyx()[0]+1, 0)
        screen.addstr(f"score={self.score}")
        for y in self.map:
            screen.move(screen.getyx()[0]+1, 0)
            for x in y:
                if(x == WALL):
                    pass
                elif(x == FOOD):
                    screen.addstr(current_food)
                elif(x == SNAKE_DOT):
                    screen.addstr('\U00002B1C') # "⬜"
                elif(x == FREE_SPACE):
                    screen.addstr('\U00002B1B') # "⬛"
                elif(x == GHOST):
                    screen.addstr('\U0001F47B') # "👻"
                else:
                    screen.addstr(f"{x} ")
        screen.move(0,0)
        screen.refresh()
    
    def print_game_over(self):
        game_over_message = list([" you lost :( ", "snek dead :( ", "game over :( ", " you suck :P ", "rm -rf / ..."][random.randint(0,4)])
        msg_index = 0

        for i in range(self.size//2-6, self.size//2+6):
            self.map[self.size//2-1][i] = " "
            self.map[self.size//2][i] = game_over_message[msg_index]
            self.map[self.size//2+1][i] = " "
            msg_index+=1
        screen.clear()
        self.print_map()
        time.sleep(3)
        screen.clear()

    
    def update_dots(self):
        for dot in self.snake_dots:
            if(dot.decrease_lifetime()):
                self.map[dot.y][dot.x] = FREE_SPACE
                self.snake_dots.remove(dot)


def change_direction(direction):
    global current_direction, direction_changed

    if (current_direction == RIGHT or current_direction == LEFT) and direction_changed == False:
        current_direction = direction if direction == UP or direction == DOWN else current_direction
    elif (current_direction == UP or current_direction == DOWN) and direction_changed == False:
        current_direction = direction if direction == RIGHT or direction == LEFT else current_direction
    direction_changed = True

def move_snake():
    if current_direction == RIGHT:
        return (x_cur+1, y_cur)
    elif current_direction == DOWN:
        return (x_cur, y_cur+1)
    elif current_direction == LEFT:
        return (x_cur-1, y_cur)
    elif current_direction == UP:
        return (x_cur, y_cur-1)

def on_press():
    global direction_changed
    event = screen.getch()
    if(event == ord('w') or event == curses.KEY_UP):
        change_direction(UP)
    elif(event == ord('d') or event == curses.KEY_RIGHT):
        change_direction(RIGHT)
    elif(event == ord('s') or event == curses.KEY_DOWN):
        change_direction(DOWN)
    elif(event == ord('a') or event == curses.KEY_LEFT):
        change_direction(LEFT)
    elif(event == ord('p')):
        while(True):
            event = screen.getch()
            if(event == ord('p')):
                break
            time.sleep(0.5)
    direction_changed = False

def countdown():
    screen.clear()
    screen.addstr("3...")
    screen.refresh()
    time.sleep(1)
    screen.clear()
    screen.addstr("2..")
    screen.refresh()
    time.sleep(1)
    screen.clear()
    screen.addstr("1.")
    screen.refresh()
    time.sleep(1)
    screen.clear()
    screen.addstr("snek 🐍")
    screen.refresh()
    time.sleep(1)
    screen.clear()

def get_random_fruit(): return AVAILABLE_FOOD[random.randint(0,len(AVAILABLE_FOOD)-1)]

if __name__ == "__main__":
    screen = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    screen.keypad(1)
    screen.nodelay(1)

    #countdown()

    current_direction = RIGHT
    x_cur, y_cur = MAP_SIZE//2-1, MAP_SIZE//2

    game_map = Map()
    game_on = True

    while (game_on):
        x_cur, y_cur = move_snake()
        game_on = game_map.set_snake_location(x=x_cur, y=y_cur)
        if(game_on):
            game_map.update_dots()
            game_map.add_new_ghost()
            game_map.set_ghost_location()
            game_map.print_map()
            time.sleep(1/VELOCITY)
            on_press()
    game_map.print_game_over()
    curses.endwin()