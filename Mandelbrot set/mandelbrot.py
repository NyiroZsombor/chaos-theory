import pygame as pg
import math
from time import time
from multiprocessing import Pool

class MandelbrotSet:

    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.surface = pg.Surface((self.size_x, self.size_y))
        self.offset_x: float = 0
        self.offset_y: float = 0
        self.set_zoom(1)
        self.background_color: tuple[int] = (0, 0, 0)
        self.color_gradient: tuple[tuple[int]] = (
            (0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255)
        )
        self.fill_color: tuple[int] = (0, 0, 0)
        self.depth: int = 20


    def set_zoom(self, z: float) -> None:
        self.zoom = z
        self.scale_x: float = 8 / ((2 ** self.zoom) * self.size_x)
        self.scale_y: float = 8 / ((2 ** self.zoom) * self.size_y)


    def set_offset_x(self, x: float) -> None:
        self.offset_x = x


    def set_offset_y(self, y: float) -> None:
        self.offset_y = y


    def set_depth(self, d: int) -> None:
        self.depth = d


    def render(self) -> None:
        start: float = time()
        size_x2: float = self.size_x / 2
        size_y2: float = self.size_y / 2
        scale_offset_x: float = self.offset_x / self.scale_x
        scale_offset_y: float = self.offset_y / self.scale_y
        min_x: int = int(-size_x2 + scale_offset_x)
        max_x: int = int(size_x2 + scale_offset_x)
        min_y: int = int(-size_y2 + scale_offset_y)
        max_y: int = int(size_y2 + scale_offset_y)

        for b in range(min_y, max_y):
            # if b % (size // 8) == 0:
            #   surf.blit(self.surface)
            #   yield
            for a in range(min_x, max_x):
                c: complex = complex(a * self.scale_x, b * self.scale_y)
                div: int = MandelbrotSet.get_divergence(c, self.depth)
                t: float = math.sqrt(div / self.depth)
                
                x: int = int(a + size_x2 - scale_offset_x)
                y: int = int(b + size_y2 - scale_offset_y)
                color: tuple[int] = MandelbrotSet.lerp_color(
                    self.color_gradient, t
                )

                self.surface.set_at((x, y), color)

        print(f"\trender took {round(time() - start, 2)} seconds")


    def get_divergence(c: complex, depth: int) -> int:
        z = 0
        for i in range(depth):
            z = z*z + c
            if abs(z) > 2: return i

        return depth
    

    def get_divergence_array(self) -> list[float]:
        # start: float = time()
        size_x2: int = int(self.size_x / 2)
        size_y2: int = int(self.size_y / 2)
        scale_offset_x: int = int(self.offset_x / self.scale_x)
        scale_offset_y: int = int(self.offset_y / self.scale_y)
        min_x: int = -size_x2 + scale_offset_x
        max_x: int = size_x2 + scale_offset_x
        min_y: int = -size_y2 + scale_offset_y
        max_y: int = size_y2 + scale_offset_y

        with Pool() as pool:
            return pool.map(get_div, [(self.scale_x, self.scale_y, self.depth, a, b)
                for b in range(min_y, max_y)
                for a in range(min_x, max_x)
            ])

        # print(f"\trender took {round(time() - start, 2)} seconds")
        # return array


    def lerp_color(gradient: tuple[tuple[int]], t: float) -> tuple[float]:
        if t > 1 or t < 0:
            print("invalid value for t", t)
            raise ValueError

        if len(gradient) < 2:
            print("invalid gradient length", len(gradient))
            raise ValueError
        
        n = len(gradient)
        segment_length: float = 1 / (n - 1)
        idx: int = min(int(t // segment_length), n - 2)
        t_local = (t - idx * segment_length) / segment_length

        c1, c2 = gradient[idx], gradient[idx + 1]
        r = (1 - t_local) * c1[0] + t_local * c2[0]
        g = (1 - t_local) * c1[1] + t_local * c2[1]
        b = (1 - t_local) * c1[2] + t_local * c2[2]

        return (r, g, b)
    
def get_div(args: any) -> float:
    scale_x, scale_y, depth, a, b = args
    c: complex = complex(a * scale_x, b * scale_y)
    div: int = MandelbrotSet.get_divergence(c, depth)
    t: float = math.sqrt(div / depth)
    
    # x: int = int(a + size_x2 - scale_offset_x)
    # y: int = int(b + size_y2 - scale_offset_y)
    return t
