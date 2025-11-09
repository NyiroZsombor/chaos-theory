import cv2
import time
import pygame as pg
from utils import *
from .pendulum import Pendulum

fps = 24
width, height = 512, 512
screen = pg.surface.Surface((width, height))
path_surf = pg.surface.Surface((width, height))
path_surf.fill("white")

filename = "output.avi"
fourcc = cv2.VideoWriter_fourcc(*"FFV1")
video = cv2.VideoWriter(filename, fourcc, fps, (width, height))

speed = 1024
n = 1
pendulums = [
    Pendulum(
        height // 5, height // 5, 1.0, 1.0,
        3.1415 / 2, 3.1415 / 2 + 3 + i / 50,
        0, 0,
        color=color_blend(((0, 255, 0), (0, 0, 255)), (i + 1) / n)
    ) for i in range(n)
]

running = fps * 10
monotonic = 0
i = 0
print("remaining / completed:\033[?25l")

while running:
    print(f"\033[1K\r{running} / {i}", end="", flush=True)
    monotonic += 1 / fps
    i += 1
    running -= 1

    for pendulum in pendulums:
        if running > fps * 2:
            pendulum.step(speed // fps, path_surf)
        else:
            pendulum.step(speed * running // (fps * fps * 2), path_surf)

        screen.blit(path_surf, (0, 0))

    for pendulum in pendulums:
        pendulum.draw_sticks(screen)
        pendulum.draw_heads(screen, 8)

    render_to_video(screen, video)

save_video(video, filename)