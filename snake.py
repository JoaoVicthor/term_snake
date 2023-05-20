import keyboard, time, os, random

UP, RIGHT, DOWN, LEFT = range(4)
FREE_SPACE, SNAKE_DOT, FOOD, WALL, GHOST = range(5)
AVAILABLE_FOOD = ("🍆","🍒","🍌","🍑")
FRAMETIME = 1000000000

MAP_SIZE = 30 # Defines map area
VELOCITY = 12 # Set intended FPS here...

TOTAL_GHOST_FRAMES = VELOCITY * 5

class SnakeDot:
    def __init__(self, x, y, lifetime):
        self.x = x
        self.y = y
        self.lifetime = lifetime
    
    def decrease_lifetime(self):
        self.lifetime -= 1
        return True if self.lifetime == 0 else False


class Map:
    def __init__(self):
        self.size = MAP_SIZE
        self.score = 0
        self.map = [[FREE_SPACE] * self.size for _ in range(self.size)]
        self.snake_dots = []
        self.ghost_frames = 0
        self.ghost_location = (0,0)

        for i in range(self.size):
            self.map[i][0] = WALL
            self.map[0][i] = WALL
            self.map[self.size-1][i] = WALL
            self.map[i][self.size-1] = WALL

        self.set_food_location()

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
        if(self.ghost_frames == TOTAL_GHOST_FRAMES):
            if(self.ghost_location != (0,0)):
                self.map[self.ghost_location[1]][self.ghost_location[0]] = FREE_SPACE
                self.ghost_location = (0,0)
            random_number = random.randint(0, int(MAP_SIZE**2*0.75))
            if(random_number < self.score):
                self.ghost_location = self.get_free_space(GHOST)
                self.map[self.ghost_location[1]][self.ghost_location[0]] = GHOST
            self.ghost_frames = 0
        else:
            self.ghost_frames+=1

    def set_snake_location(self, x, y):
        if(self.map[y][x] == FREE_SPACE):
            self.map[y][x] = SNAKE_DOT
            self.snake_dots.append(SnakeDot(x,y,3+self.score))
            return True
        elif(self.map[y][x] == FOOD):
            self.score+=1
            self.map[y][x] = SNAKE_DOT
            self.set_food_location()
            self.snake_dots.append(SnakeDot(x,y,3+self.score))
            return True
        elif(self.map[y][x] == SNAKE_DOT or self.map[y][x] == WALL or self.map[y][x] == GHOST):
            return False
        
    def print_map(self):
        global current_food

        print(f"\nscore={self.score}")
        for y in self.map:
            for x in y:
                if(x == WALL):
                    pass
                elif(x == FOOD):
                    print(current_food, end='')
                elif(x == SNAKE_DOT):
                    print("⬜", end='')
                elif(x == FREE_SPACE):
                    print("⬛", end='')
                elif(x == GHOST):
                    print("👻", end='')
                else:
                    print(f"{x} ", end='')
            print()
    
    def print_game_over(self):
        game_over_message = list([" you lost :( ", "snek dead :( ", "game over :( ", " you suck :P ", "rm -rf / ..."][random.randint(0,4)])
        msg_index = 0

        for i in range(self.size//2-6, self.size//2+6):
            self.map[self.size//2-1][i] = " "
            self.map[self.size//2][i] = game_over_message[msg_index]
            self.map[self.size//2+1][i] = " "
            msg_index+=1
        os.system('clear')
        self.print_map()
        time.sleep(3)
        os.system('clear')

    
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
    end_time = time.time_ns() + FRAMETIME/VELOCITY

    while(time.time_ns() < end_time):
        if(keyboard.is_pressed('w') or keyboard.is_pressed('up')):
            change_direction(UP)
        elif(keyboard.is_pressed('d') or keyboard.is_pressed('right')):
            change_direction(RIGHT)
        elif(keyboard.is_pressed('s') or keyboard.is_pressed('down')):
            change_direction(DOWN)
        elif(keyboard.is_pressed('a') or keyboard.is_pressed('left')):
            change_direction(LEFT)
    direction_changed = False

def countdown():
    os.system('clear')
    print("3...")
    time.sleep(1)
    os.system('clear')
    print("2..")
    time.sleep(1)
    os.system('clear')
    print("1.")
    time.sleep(1)
    os.system('clear')
    print("snek 🐍")
    time.sleep(1)
    os.system('clear')

def get_random_fruit(): return AVAILABLE_FOOD[random.randint(0,len(AVAILABLE_FOOD)-1)]

if __name__ == "__main__":
    countdown()

    current_direction = RIGHT
    x_cur, y_cur = MAP_SIZE//2-1, MAP_SIZE//2

    game_map = Map()
    game_on = True

    while (game_on):
        x_cur, y_cur = move_snake()
        game_on = game_map.set_snake_location(x=x_cur, y=y_cur)
        if(game_on):
            game_map.update_dots()
            game_map.set_ghost_location()
            os.system('clear')
            game_map.print_map()
            on_press()

    game_map.print_game_over()