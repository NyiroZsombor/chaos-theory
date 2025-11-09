import pygame as pg
from utils import *
from .mandelbrot import MandelbrotSet

width, height = 640, 640
screen = pg.surface.Surface((width, height))
mb = MandelbrotSet(width, height)
mb.set_offset_x(-0.5988473510742187)
mb.set_offset_y(-0.6645997314453126)

fps = 2
filename = "output.avi"
fourcc = cv2.VideoWriter_fourcc(*"FFV1")
video = cv2.VideoWriter(filename, fourcc, fps, (width, height))

max_depth = 1200
min_depth = 120
max_zoom = 20
running = int(fps * 16)
num_frames = running
i = 0
completion = 0
print("remaining / completed:\033[?25l")

while running:
    print(f"\033[1K\r{running} / {i}", end="", flush=False)
    print(f" ({round(completion * 100)}%)", end="", flush=True)
    running -= 1
    i += 1
    completion = i / (running + i)

    mb.set_zoom(completion * max_zoom)
    mb.set_depth(int(min_depth + completion * (max_depth - min_depth)))
    print(f"depth: {mb.depth}")
    arr = mb.get_divergence_array()

    for y in range(height):
        for x in range(width):
            t = arr[y * width + x]
            screen.set_at((x, y), MandelbrotSet.lerp_color(
                mb.color_gradient, t
            ))

    render_to_video(screen, video)

# pg.image.save(screen, create_filename("output", "png"), "png")
save_video(video, filename)
