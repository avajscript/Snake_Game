import pygame as pg
import copy
import random

from DoublyLinkedList import DoublyLinkedList
from DoublyLinkedList import Node

pg.init()

# screen dimensions
BOARD_WIDTH = 400
COLUMNS = 10
BLOCK_WIDTH = BOARD_WIDTH / COLUMNS

# colors
DARK_PURPLE = (48, 0, 80)
PURPLE = (83, 2, 137)
COLORS_TUPLE = (DARK_PURPLE, PURPLE)
SNAKE_COLOR = (148, 255, 122)
APPLE_COLOR = (255, 122, 122)

class TestNode:
    def __init__(self, num):
        self.num = num

    def print_msg(self):
        print(f"Num: {self.num}")



class Segment(Node):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def set_point(self, point):
        self.x, self.y = point


class Snake:
    def __init__(self, color, block_width):
        self.list = DoublyLinkedList()
        self.color = color
        self.initialize_snake()
        self.block_width = block_width
        self.dir = "right"

    def initialize_snake(self):
        self.list.insert_end(Segment(5, 5))
        self.list.insert_end(Segment(4, 5))
        self.list.insert_end(Segment(3, 5))

    def move_snake(self):
        # update the head position
        head_copy = copy.copy(self.list.head)
        if self.dir == "right":
            if head_copy.x < COLUMNS:
                head_copy.x += 1
        elif self.dir == "left":
            if head_copy.x > 0:
                head_copy.x -= 1
        elif self.dir == "up":
            if head_copy.y > 0:
                head_copy.y -= 1
        elif self.dir == "down":
            if head_copy.y < COLUMNS:
                head_copy.y += 1

        current = self.list.head
        prev_values = (current.x, current.y)
        current.x = head_copy.x
        current.y = head_copy.y
        current = current.next

        while current:
            temp_values = (current.x, current.y)
            current.set_point(prev_values)
            prev_values = temp_values
            current = current.next

    def add_segment(self):
        tail = self.list.tail
        x = tail.x
        y = tail.y

        if self.dir == "right":
            x = tail.x - 1
        elif self.dir == "left":
            x = tail.x + 1
        elif self.dir == "up":
            y = tail.y + 1
        elif self.dir == "down":
            x = tail.y - 1

        segment = Segment(x, y)
        self.list.insert_end(segment)

    def check_collision(self):
        collision_state = False
        head = self.list.head
        current = head.next

        while current:
            if head.x == current.x and head.y == current.y:
                collision_state = True
                break
            current = current.next

        return collision_state
    def draw(self, surface):
        segment = self.list.head
        while segment:
            pg.draw.rect(surface, self.color, (segment.x * self.block_width, segment.y * self.block_width,
                                               self.block_width, self.block_width))
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
        surface.blit(self.surface, (0, 0))

    def gameCycle(self, surface):
        if not self.playing:
            return
        # update the game state
        snake_head = self.snake.list.head
        snake_head_pos = (snake_head.x, snake_head.y)
        apple_pos = (apple.x, apple.y)

        # snake head over apple position
        if snake_head_pos == apple_pos:
            apple.move_random()
            snake.add_segment()
            if snake.check_collision():
                self.playing = False

        # draw the game objects
        self.draw(surface)
        self.snake.draw(surface)
        self.apple.draw(surface)
class Apple:
    def __init__(self, color, x, y, block_width):
        self.color = color
        self.x = x
        self.y = y
        self.block_width = block_width

    def draw(self, surface):
        pg.draw.rect(surface, self.color, (self.x * self.block_width, self.y * self.block_width,
                                                self.block_width, self.block_width))

    def move_random(self):
        rx = random.randint(0, 9)
        ry = random.randint(0, 9)
        self.x = rx
        self.y = ry


# game state
running = True

# game objects
screen = pg.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
snake = Snake(SNAKE_COLOR, BLOCK_WIDTH)
apple = Apple(APPLE_COLOR, 6, 6, BLOCK_WIDTH)
board = Board(snake, apple, BOARD_WIDTH, COLUMNS, BLOCK_WIDTH)

board.draw(screen)
snake.draw(screen)
apple.draw(screen)
pg.display.update()


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                snake.dir = "up"
                snake.move_snake()
            elif event.key == pg.K_d:
                snake.dir = "right"
                snake.move_snake()
            elif event.key == pg.K_s:
                snake.dir = "down"
                snake.move_snake()
            elif event.key == pg.K_a:
                snake.dir = "left"
                snake.move_snake()

            board.gameCycle(screen)
            pg.display.update()


