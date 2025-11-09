from math import *

class Cam:
    angle_x = -pi / 6
    angle_z = 0
    x = 0
    y = 0
    z = tan(angle_x) - 16

    @staticmethod
    def draw_debug(surf, font):
        x = 6
        y = 0
        for attr, val in vars(Cam).items():
            if attr.startswith("_"): continue
            if type(val) != float: continue
            text = font.render(f"{attr}: {val}", True, "black")
            surf.blit(text, (x, y))
            y += text.get_height()