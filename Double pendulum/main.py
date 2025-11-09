import pygame as pg
from utils import *
from .pendulum import Pendulum

fps = 30
width, height = 512, 512
screen = pg.display.set_mode((width, height))
path_surf = pg.surface.Surface((width, height))
path_surf.fill("white")
clock = pg.time.Clock()

n = 4
pendulums = [
    Pendulum(
        height // 5, height // 5, 1.0, 1.0,
        2.49, 0.25 + i / 1_000_000_000,
        0, 0,
        color=color_blend(((0, 255, 0), (0, 0, 255)), i / (n - 1))
    ) for i in range(n)
]
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for pendulum in pendulums:
        pendulum.step(32, path_surf)
        screen.blit(path_surf, (0, 0))

    for pendulum in pendulums:
        pendulum.draw_sticks(screen)
        pendulum.draw_heads(screen, 8)

    pg.display.flip()
    clock.tick(fps)

pg.quit()