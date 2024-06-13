import os

import pygame as pg
import copy
import random

from DoublyLinkedList import DoublyLinkedList
from DoublyLinkedList import Node

pg.init()

clock = pg.time.Clock()
fps = 60





# fonts
font = pg.font.Font(None, 24)

# screen dimensions
BOARD_WIDTH = 400
COLUMNS = 10
BLOCK_WIDTH = BOARD_WIDTH / COLUMNS
BORDER_WIDTH = 40

screen = pg.display.set_mode((BOARD_WIDTH + BORDER_WIDTH * 2, BOARD_WIDTH + BORDER_WIDTH * 2))


# colors
DARK_PURPLE = (48, 0, 80)
PURPLE = (83, 2, 137)
LIGHT_PURPLE = (193, 104, 253)
COLORS_TUPLE = (DARK_PURPLE, PURPLE)
SNAKE_COLOR = (148, 255, 122)
APPLE_COLOR = (255, 122, 122)

# game state
running = True
alive = True
score = 0
SCORE_INCREMENT = 1
SCORE_INCREASE_ITERATION = 50
frame_anim_iteration = 15
frame_count = 0

# load images

# load planets
baren_img = pg.image.load("graphics/planets/Baren.png").convert_alpha()
black_hole_img = pg.image.load("graphics/planets/Black_hole.png").convert_alpha()
ice_img = pg.image.load("graphics/planets/Ice.png").convert_alpha()
lava_img = pg.image.load("graphics/planets/Lava.png").convert_alpha()
terran_img = pg.image.load("graphics/planets/Terran.png").convert_alpha()

# animations

explosion_4_images = []
explosion_path = "graphics/animations/explosion_4"
files = os.listdir(explosion_path)
for file in files:
    explosion_4_images.append(pg.transform.scale(pg.image.load(os.path.join(explosion_path, file)), (32, 32)))

# resize images
baren_img = pg.transform.scale(baren_img, (32, 32))
black_hole_img = pg.transform.scale(black_hole_img, (32, 32))
ice_img = pg.transform.scale(ice_img, (32, 32))
lava_img = pg.transform.scale(lava_img, (32, 32))
terran_img = pg.transform.scale(terran_img, (32, 32))

planet_images = (baren_img, black_hole_img, ice_img, lava_img, terran_img)
planets_length = len(planet_images) - 1


# load snake images
body_bottomleft_img = pg.image.load("graphics/body_bottomleft.png").convert_alpha()
body_bottomright_img = pg.image.load("graphics/body_bottomright.png").convert_alpha()
body_horizontal_img = pg.image.load("graphics/body_horizontal.png").convert_alpha()
body_topleft_img = pg.image.load("graphics/body_topleft.png").convert_alpha()
body_topright_img = pg.image.load("graphics/body_topright.png").convert_alpha()
body_vertical_img = pg.image.load("graphics/body_vertical.png").convert_alpha()
head_down_img = pg.image.load("graphics/head_down.png").convert_alpha()
head_left_img = pg.image.load("graphics/head_left.png").convert_alpha()
head_right_img = pg.image.load("graphics/head_right.png").convert_alpha()
head_up_img = pg.image.load("graphics/head_up.png").convert_alpha()
tail_down_img = pg.image.load("graphics/tail_down.png").convert_alpha()
tail_left_img = pg.image.load("graphics/tail_left.png").convert_alpha()
tail_right_img = pg.image.load("graphics/tail_right.png").convert_alpha()
tail_up_img = pg.image.load("graphics/tail_up.png").convert_alpha()


head_images = (head_up_img, head_right_img, head_down_img, head_left_img)
tail_images = (tail_up_img, tail_right_img, tail_down_img, tail_left_img)
body_images = (body_vertical_img, body_bottomright_img, body_horizontal_img, body_bottomleft_img, body_vertical_img,
               body_topleft_img, body_horizontal_img, body_topright_img)

class TestNode:
    def __init__(self, num):
        self.num = num

    def print_msg(self):
        print(f"Num: {self.num}")



class Segment(Node):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image

    def set_point(self, point):
        self.x, self.y = point


class Snake:
    def __init__(self, color, block_width):
        self.list = DoublyLinkedList()
        self.color = color
        self.initialize_snake()
        self.block_width = block_width
        self.dir = "right"
        self.prev_dir = "right"
        self.tail_prev = (0, 0)

    def initialize_snake(self):
        self.list.insert_end(Segment(5, 5, head_images[1]))
        self.list.insert_end(Segment(4, 5, body_images[2]))
        self.list.insert_end(Segment(3, 5, body_images[2]))

    def move_snake(self):
        self.tail_prev = (self.list.tail.x, self.list.tail.y)
        # update the head position
        current = copy.copy(self.list.head)
        head = self.list.head
        if self.dir == "right":
            if head.x < COLUMNS:
                head.image = head_images[1]
                head.x += 1
        elif self.dir == "left":
            head.image = head_images[3]
            if head.x > 0:
                head.x -= 1
        elif self.dir == "up":
            head.image = head_images[0]
            if head.y > 0:
                head.y -= 1
        elif self.dir == "down":
            head.image = head_images[2]
            if head.y < COLUMNS:
                head.y += 1

        if self.dir == self.prev_dir:
            print("prev")
            if self.dir == "right" or self.dir == "left":
                new_image = body_images[2]
            else:
                new_image = body_images[0]
        else:
            print("not prev")
            if self.dir == "right":
                if self.prev_dir == "up":
                    new_image = body_images[1]
                else:
                    new_image = body_images[7]
            if self.dir == "left":
                if self.prev_dir == "up":
                    new_image = body_images[3]
                else:
                    new_image = body_images[5]
            if self.dir == "up":
                if self.prev_dir == "right":
                    new_image = body_images[5]
                else:
                    new_image = body_images[7]
            if self.dir == "down":
                if self.prev_dir == "right":
                    new_image = body_images[3]
                else:
                    new_image = body_images[1]

        self.prev_dir = self.dir
        cur_x, cur_y, cur_img = current.x, current.y, new_image
        current = current.next
        while current:
            temp_x, temp_y, temp_img = current.x, current.y, current.image
            current.x, current.y, current.image = cur_x, cur_y, cur_img
            current = current.next
            cur_x, cur_y, cur_img = temp_x, temp_y, temp_img




        self.list.print_nodes()
    def add_segment(self):
        tail = self.list.tail
        x_dif = tail.x - self.tail_prev[0]
        y_dif = tail.y - self.tail_prev[1]
        if x_dif > 0:
            tail_img = tail_images[3]
        if x_dif < 0:
            tail_img = tail_images[1]
        if y_dif > 0:
            tail_img = tail_images[0]
        if y_dif < 0:
            tail_img = tail_images[2]

        segment = Segment(self.tail_prev[0], self.tail_prev[1], tail_img)
        self.list.insert_end(segment)

    def hit_animation(self, node, first_run=True, color=None):
        if first_run:
            color = list(SNAKE_COLOR)
            self.hit_animation(node, False, color)
        else:
            red = color[0]
            red = min(255, red + 1)
            
    def check_collision(self):
        collision_state = False
        head = self.list.head
        current = head.next

        while current:
            if head.x == current.x and head.y == current.y:
                collision_state = True
                global alive
                alive = False
                break
            current = current.next

        return collision_state
    def draw(self, surface):
        segment = self.list.head
        while segment:
            surface.blit(segment.image, (segment.x * self.block_width, segment.y * self.block_width))
            segment = segment.next


class Board:
    def __init__(self, snake, apple, width, columns, block_width):
        self.surface = pg.Surface((width, width))
        self.width = width
        self.columns = columns
        self.block_width = block_width
        self.snake = snake
        self.apple = apple
        self.score = 0
        self.playing = True

    def draw(self, surface):
        for y in range(COLUMNS):
            for x in range(COLUMNS):
                pg.draw.rect(self.surface, COLORS_TUPLE[(x + y) % 2 == 0],
                             (x * self.block_width, y * self.block_width, self.block_width, self.block_width))

    def game_cycle(self, surface):
        if not self.playing:
            return
        # update the game state
        snake_head = self.snake.list.head
        snake_head_pos = (snake_head.x, snake_head.y)
        apple_pos = (apple.x, apple.y)
        if snake.check_collision():
            self.playing = False
        # snake head over apple position
        if snake_head_pos == apple_pos:
            apple.move_random()
            snake.add_segment()
            global score
            score += SCORE_INCREMENT


        # draw the game objects
        self.draw(surface)
        self.snake.draw(self.surface)
        self.apple.draw(self.surface)
        draw_menu(surface)
        surface.blit(self.surface, (BORDER_WIDTH, BORDER_WIDTH))


class Apple:
    def __init__(self, image, x, y, block_width):
        self.image = image
        self.x = x
        self.y = y
        self.block_width = block_width




    def draw(self, surface):
        surface.blit(self.image, (self.x * self.block_width + 4, self.y * self.block_width + 4))

    def move_random(self):
        self.image = planet_images[random.randint(0, planets_length)]
        rx = random.randint(0, 9)
        ry = random.randint(0, 9)
        self.x = rx
        self.y = ry



class AnimationRunner:
    def __init__(self, image_array):
        self.x = None
        self.y = None
        self.start_time = None
        self.image_array = image_array

        


def draw_menu(screen):
    score_label = font.render(f"Score: {score}", True, DARK_PURPLE)

    pg.draw.rect(screen, LIGHT_PURPLE, (0, 0, BOARD_WIDTH + BORDER_WIDTH * 2, BOARD_WIDTH + BORDER_WIDTH * 2))
    screen.blit(score_label, (5, 5))


# game objects
pg.draw.rect(screen, LIGHT_PURPLE, (0, 0, BOARD_WIDTH + BORDER_WIDTH * 2, BOARD_WIDTH + BORDER_WIDTH * 2))
snake = Snake(SNAKE_COLOR, BLOCK_WIDTH)
apple = Apple(planet_images[random.randint(0, planets_length)], 6, 6, BLOCK_WIDTH)
board = Board(snake, apple, BOARD_WIDTH, COLUMNS, BLOCK_WIDTH)


board.game_cycle(screen)
pg.display.update()




while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                snake.dir = "up"
            elif event.key == pg.K_d:
                snake.dir = "right"
            elif event.key == pg.K_s:
                snake.dir = "down"
            elif event.key == pg.K_a:
                snake.dir = "left"
    if alive:
        frame_count += 1
        if frame_count > frame_anim_iteration:
            frame_count = 0
            snake.move_snake()
            board.game_cycle(screen)
            pg.display.update()
    
    
    clock.tick(fps)

