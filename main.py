import tkinter as tk

from gamelib import Sprite, GameApp, Text

from dir_consts import *
from maze import Maze

import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

UPDATE_DELAY = 33

PACMAN_SPEED = 5

class Pacman(Sprite):
    def __init__(self, app, maze, r, c):
        self.r = r
        self.c = c
        self.maze = maze
        self.dot_eaten_observers = []

        self.direction = DIR_STILL
        self.next_direction = DIR_STILL

        x, y = maze.piece_center(r,c)
        super().__init__(app, 'images/pacman.png', x, y)

        self.state = NormalPacmanState(self)

    def update(self):
        if self.maze.is_at_center(self.x, self.y):
            r, c = self.maze.xy_to_rc(self.x, self.y)

            if self.maze.has_dot_at(r, c):
                self.maze.eat_dot_at(r, c)
                self.dot_eaten_observers[0]()

                self.state.random_upgrade()

            if self.maze.is_movable_direction(r, c, self.next_direction):
                self.direction = self.next_direction
            else:
                self.direction = DIR_STILL

        self.state.move_pacman()

    def set_next_direction(self, direction):
        self.next_direction = direction


class PacmanGame(GameApp):
    def init_game(self):
        self.maze = Maze(self, CANVAS_WIDTH, CANVAS_HEIGHT)

        self.pacman1 = Pacman(self, self.maze, 1, 1)
        self.pacman2 = Pacman(self, self.maze, self.maze.get_height() - 2, self.maze.get_width() - 2)
        self.pacman1.dot_eaten_observers.append(self.dot_eaten_by_pacman1)
        self.pacman2.dot_eaten_observers.append(self.dot_eaten_by_pacman2)
        self.pacman1_score_text = Text(self, 'P1: 0', 100, 20)
        self.pacman2_score_text = Text(self, 'P2: 0', 600, 20)

        self.elements.append(self.pacman1)
        self.elements.append(self.pacman2)
        self.pacman1_score = 0
        self.pacman2_score = 0

    def dot_eaten_by_pacman1(self):
        self.pacman1_score += 1
        self.update_scores()

    def dot_eaten_by_pacman2(self):
        self.pacman2_score += 1
        self.update_scores()

    def update_scores(self):
        self.pacman1_score_text.set_text(f'P1: {self.pacman1_score}')
        self.pacman2_score_text.set_text(f'P2: {self.pacman2_score}')

        self.command_map = {
            'W': self.get_pacman_next_direction_function(self.pacman1, DIR_UP),
            'S': self.get_pacman_next_direction_function(self.pacman1, DIR_DOWN),
            'D': self.get_pacman_next_direction_function(self.pacman1, DIR_RIGHT),
            'A': self.get_pacman_next_direction_function(self.pacman1, DIR_LEFT),

            'I': self.get_pacman_next_direction_function(self.pacman2, DIR_UP),
            'K': self.get_pacman_next_direction_function(self.pacman2, DIR_DOWN),
            'L': self.get_pacman_next_direction_function(self.pacman2, DIR_RIGHT),
            'J': self.get_pacman_next_direction_function(self.pacman2, DIR_LEFT),
        }

    def pre_update(self):
        pass

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        ch = event.char.upper()

        if ch in self.command_map:
            self.command_map[ch]()


    def get_pacman_next_direction_function(self, pacman, next_direction):
        def f():
            pacman.set_next_direction(next_direction)
        return f


class NormalPacmanState:
    def __init__(self, pacman):
        self.pacman = pacman

    def random_upgrade(self):
        if random.random() < 0.1:
            self.pacman.state = SuperPacmanState(self.pacman)

    def move_pacman(self):
        self.pacman.x += PACMAN_SPEED * DIR_OFFSET[self.pacman.direction][0]
        self.pacman.y += PACMAN_SPEED * DIR_OFFSET[self.pacman.direction][1]


class SuperPacmanState:
    def __init__(self, pacman):
        self.pacman = pacman
        self.counter = 0

    def random_upgrade(self):
        if self.counter >= 50:
            self.pacman.state = NormalPacmanState(self.pacman)
        self.counter += 1

    def move_pacman(self):
        self.pacman.x += 2 * PACMAN_SPEED * DIR_OFFSET[self.pacman.direction][0]
        self.pacman.y += 2 * PACMAN_SPEED * DIR_OFFSET[self.pacman.direction][1]


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pacman")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = PacmanGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
