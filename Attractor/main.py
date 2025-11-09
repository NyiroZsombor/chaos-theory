import sys
import pygame as pg
from math import *
from .cam import Cam
from utils import *
from time import monotonic
from .attractor import Attractor

pg.init()
pg.font.init()
debug = not (len(sys.argv) > 1 and sys.argv[1] == "-r")

width, height = (1080, 1080) if debug else (1080, 1080)
if debug:
    render_scale = 2
else:
    render_scale = 1
screen = pg.display.set_mode((width, height))
debug_surf = pg.surface.Surface((width, height))
clock = pg.time.Clock()
font = pg.font.SysFont("JetbrainsMono", 24)
fps = 60
running = True
render_surf = pg.surface.Surface((
    width // render_scale,
    height // render_scale
))

lorenz = (28, 10, 8 / 3)
attr = lorenz
steps = 3000 if debug else 6000

redish = (0x833AB4, 0xFD1D1D, 0xFCB045)
blueish = (0x2A7B9B, 0x57C785, 0xEDDD53)

l1 = Attractor(steps,
    *attr,
    # 1, 1, 1.001,
    colors=blueish)
    # 0x00FFFF,))
l2 = Attractor(steps,
    *attr,
    # 1, 1, 1,
    colors=blueish)
    # 0xFF00FF,))

l1.calculate_points()
# l2.calculate_points()

r = 96

angle_vel_x = 0
angle_vel_z = 0
vel_x = 0
vel_y = 0
vel_z = 0

rot_speed = pi / 2
speed = 32

Cam.angle_x = -0.4451
Cam.angle_z = -2.303853143350473
Cam.x =       -52.303973944494544
Cam.y =       53.55927513826341
Cam.z =       -7.510799999999997

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
            sign = 1 if event.type == pg.KEYDOWN else -1

            if event.key == pg.K_RIGHT:
                angle_vel_z -= rot_speed * sign
            elif event.key == pg.K_LEFT:
                angle_vel_z += rot_speed * sign
            elif event.key == pg.K_UP:
                angle_vel_x += rot_speed * sign
            elif event.key == pg.K_DOWN:
                angle_vel_x -= rot_speed * sign
            elif event.key == pg.K_d:
                vel_x += sign
            elif event.key == pg.K_a:
                vel_x -= sign
            elif event.key == pg.K_w:
                vel_y += sign
            elif event.key == pg.K_s:
                vel_y -= sign
            elif event.key == pg.K_LSHIFT:
                vel_z += sign
            elif event.key == pg.K_SPACE:
                vel_z -= sign

    Cam.angle_z += angle_vel_z / fps
    Cam.angle_x += angle_vel_x / fps
    Cam.x += (vel_x * cos(Cam.angle_z) - vel_y * sin(Cam.angle_z)) * speed / fps
    Cam.y += (vel_x * sin(Cam.angle_z) + vel_y * cos(Cam.angle_z)) * speed / fps
    Cam.z += vel_z * speed / fps

    # angle = monotonic() * pi / 6
    # Cam.x = cos(angle) * r
    # Cam.y = sin(angle) * r
    # Cam.angle_z = angle + pi / 2

    render_surf.fill("white")

    # l1.step(2)
    # l2.step(2)
    l1.draw(render_surf, render_scale)
    # l2.draw(render_surf, render_scale)

    screen.blit(pg.transform.scale_by(render_surf, render_scale), (0, 0))

    if debug:
        Cam.draw_debug(screen, font)

    pg.display.flip()
    clock.tick(fps)

if not debug:
    basename = "attractor"
    ext = "png"
    filename = create_filename(basename, ext)
    print(f"image saved as {filename}")
    pg.image.save(render_surf, filename, ext)
else:
    with open("cam.txt", "w") as file:
        file.writelines((
            str(Cam.angle_x), "\n",
            str(Cam.angle_z), "\n",
            str(Cam.x), "\n",
            str(Cam.y), "\n",
            str(Cam.z), "\n"
        ))

pg.quit()
