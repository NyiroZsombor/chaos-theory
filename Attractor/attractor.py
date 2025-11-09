import numpy as np
import pygame as pg
from .cam import Cam
from math import *
from utils import *
from random import random

class Attractor:
    dt = 0.01

    def __init__(self, steps,
    rho, sigma, beta,
    x=None, y=None, z=None,
    colors=None):
        self.steps = steps
        self.rho = rho
        self.sigma = sigma
        self.beta = beta
        self.x = random() if x is None else x
        self.y = random() if y is None else y
        self.z = random() if z is None else z

        self.points = np.empty([steps, 3])
        self.prev_point = None
        self.curr_i = 0

        if colors is None:
            colors = [0xFF0000, 0x0000FF]
        self.rgb_colors = [hex2rgb(c) for c in colors]
        
        # self.calculate_points()

    
    def step(self, n=1):
        if self.curr_i == self.steps: return
        n -= 1
        dx = self.sigma * (self.y - self.x)
        dy = self.x * (self.rho - self.z) - self.y
        dz = self.x * self.y - self.beta * self.z
        self.x += self.dt * dx
        self.y += self.dt * dy
        self.z += self.dt * dz
        self.points[self.curr_i] = np.array([self.x, self.y, self.z])
        self.curr_i += 1
        if n > 0: self.step(n)

    
    def calculate_points(self):
        for _ in range(self.steps):
            self.step()

    @staticmethod
    def transform_point(x, y, z):
        x -= Cam.x
        z -= Cam.z
        y -= Cam.y

        tx = +cos(Cam.angle_z) * x + sin(Cam.angle_z) * y
        ty = -sin(Cam.angle_z) * x + cos(Cam.angle_z) * y
        x = tx
        y = ty

        tz = +cos(Cam.angle_x) * z + sin(Cam.angle_x) * y
        ty = -sin(Cam.angle_x) * z + cos(Cam.angle_x) * y
        z = tz
        y = ty

        if y <= 0: return None
        # y /= 32

        return x, y, z

    def draw_point(self, i, surf, scale):
        focal_length = 1024

        t = self.transform_point(*self.points[i])
        if t is None:
            self.prev_point = None
            return
        if self.prev_point is None:
            self.prev_point = t
            return

        px, py, pz = self.prev_point
        x, y, z = t
        self.prev_point = t

        start = (
            int(px / py * focal_length // scale + surf.get_width() // 2),
            int(pz / py * focal_length // scale + surf.get_height() // 2)
        )
        end = (
            int(x / y * focal_length // scale + surf.get_width() // 2),
            int(z / y * focal_length // scale + surf.get_height() // 2)
        )

        # depth = exp(-(y - 4) / 2)
        # color = color_blend((0, 0, 255), (255, 0, 0), depth)
        
        color = color_blend(self.rgb_colors, i / self.steps)
        # color = color_blend((0, 0, 0), color, depth)
        pg.draw.line(surf, color, start, end, 2)


    def draw(self, surf, scale=1):
        self.prev_point = None
        for i in range(0, self.curr_i // scale, scale):
            self.draw_point(i, surf, scale)