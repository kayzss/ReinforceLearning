#! python 
# @Time    : 17-12-19
# @Author  : kay
# @File    : environment.py
# @E-mail  : 861186267@qq.com
# @Function:


import numpy as np
import tkinter as tk
import time

UNIT = 40  # pixels
MAZE_W = 4  # grid width
MAZE_H = 4  # grid height
radius = 15


class MAZE(tk.Tk):
    def __init__(self):
        super(MAZE, self).__init__()
        self.actions = ['u', 'd', 'l', 'r']  # up, down, left, right
        self.n_actions = len(self.actions)
        self.title('MAZE')
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        self.build_maze()

    def build_maze(self):

        self.canvas = tk.Canvas(self, bg='white', width=MAZE_W * UNIT, height=MAZE_H * UNIT)

        for c in range(0, MAZE_W * UNIT, UNIT):
            # draw the vertical lines
            xs, ys, xe, ye = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(xs, ys, xe, ye)

        for r in range(0, MAZE_H * UNIT, UNIT):
            # draw the horizontal lines
            xs, ys, xe, ye = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(xs, ys, xe, ye)

        # create origin
        self.origin = np.array([20, 20])

        # create hell1
        hell1_center = self.origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(hell1_center[0] - radius, hell1_center[1] - radius,
                                                  hell1_center[0] + radius, hell1_center[1] + radius,
                                                  fill='black')

        # create hell2
        hell2_center = self.origin + np.array([UNIT, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(hell2_center[0] - radius, hell2_center[1] - radius,
                                                  hell2_center[0] + radius, hell2_center[1] + radius,
                                                  fill='black')

        # create oval
        oval_center = self.origin + UNIT * 2
        self.oval = self.canvas.create_oval(oval_center[0] - radius, oval_center[1] - radius,
                                            oval_center[0] + radius, oval_center[1] + radius,
                                            fill='yellow')

        # create rect
        self.rect = self.canvas.create_rectangle(self.origin[0] - radius, self.origin[1] - radius,
                                                 self.origin[0] + radius, self.origin[1] + radius,
                                                 fill='red')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.origin[0] - radius, self.origin[1] - radius,
                                                 self.origin[0] + radius, self.origin[1] + radius,
                                                 fill='red')

        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_actions = np.array([0, 0])

        if action == 0:  # up
            if s[1] > UNIT:
                base_actions[1] -= UNIT
        elif action == 1:  # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_actions[1] += UNIT
        elif action == 2:  # left
            if s[0] > UNIT:
                base_actions[0] -= UNIT
        elif action == 3:  # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_actions[0] += UNIT

        self.canvas.move(self.rect, base_actions[0], base_actions[1])  # move action

        s_ = self.canvas.coords(self.rect)  # the position of next state

        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()
