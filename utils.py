import os
import cv2
import numpy as np
import pygame as pg
from math import *
from datetime import datetime

def hex2rgb(c):
    return (
        c >> 16,
        c >> 8 & 0xFF,
        c & 0xFF,
    )

def clamp(a, b=None, t=None):
    if b is None:
        t = a
        a = 0
        b = 1
    return min(b, max(a, t))

def lerp(a, b, t):
    return a + (b - a) * t

def linear_color_gradient(c1, c2, t):
    return (
        int(lerp(sqrt(c1[0] / 255), sqrt(c2[0] / 255), clamp(t)) ** 2 * 255),
        int(lerp(sqrt(c1[1] / 255), sqrt(c2[1] / 255), clamp(t)) ** 2 * 255),
        int(lerp(sqrt(c1[2] / 255), sqrt(c2[2] / 255), clamp(t)) ** 2 * 255)
    )

def color_blend(colors, t):
    if t == 1 or len(colors) == 1:
        return colors[-1]
    count = len(colors) - 1
    u = t * count
    ct = int(u)
    return linear_color_gradient(colors[ct], colors[ct + 1], u % 1)


def render_to_video(surf, video):
    frame = pg.surfarray.array3d(surf)
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)

def create_filename(basename, ext=None):
    now = datetime.now()
    if "." in basename:
        basename = ".".join(basename.split(".")[0:-1])

    if ext:
        return f"out/{basename} {now.date()} {now.time()}.{ext}"
    else:
        return f"out/{basename} {now.date()} {now.time()}"

def save_video(video, filename):
    print("\033[?25h")
    video.release()
    print(f"video saved as {filename}")

    converted_filename = create_filename(filename, "mp4")
    os.system(f"ffmpeg -i {filename} -vcodec libx264 -crf 18 -pix_fmt yuv420p \"{converted_filename}\"")
    os.system("rm output.avi")
    print(f"video saved as {converted_filename}")
