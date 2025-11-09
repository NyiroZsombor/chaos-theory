import cv2
import pygame as pg
from .cam import Cam
from utils import *
from math import sin, cos, pi
from .attractor import Attractor

fps = 60
width, height = 1080, 1080
screen = pg.surface.Surface((width, height))

filename = "output.avi"
fourcc = cv2.VideoWriter_fourcc(*"FFV1")
video = cv2.VideoWriter(filename, fourcc, fps, (width, height))

lorenz = (28, 10, 8 / 3)
attr = lorenz
steps = 8000

redish = (0x833AB4, 0xFD1D1D, 0xFCB045)
blueish = (0x2A7B9B, 0x57C785, 0xEDDD53)

l1 = Attractor(steps,
    *attr,
    1, 1, 1.001,
    colors=blueish
)
l2 = Attractor(steps,
    *attr,
    1, 1, 1,
    colors=redish
)

# l1.calculate_points()
# l2.calculate_points()

r = 64
speed = 480 / fps
period = 10

Cam.angle_x = -0.4451
Cam.angle_z = -2.303853143350473
Cam.x =       -52.303973944494544
Cam.y =       53.55927513826341
Cam.z =       -4

running = int(steps / speed) + fps * 2 # fps * period
num_frames = running
monotonic = 0
i = 0
print("remaining / completed:\033[?25l")

screen.fill("white")
render_to_video(screen, video)

while running:
    print(f"\033[1K\r{running} / {i}", end="", flush=True)
    monotonic += 1 / fps
    i += 1
    running -= 1

    angle = pi * 2 - running / num_frames * pi * 2 / period - pi * 5 / 4
    Cam.x = cos(angle) * r + 7
    Cam.y = sin(angle) * r
    Cam.angle_z = angle + pi / 2

    screen.fill("white")
    
    l1.step(speed)
    l2.step(speed)
    l1.draw(screen)
    l2.draw(screen)
    render_to_video(screen, video)

pg.quit()

save_video(video, filename)
