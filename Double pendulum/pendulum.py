import pygame as pg
import math

class Pendulum:
    dt = 0.01
    g = 9.81
    origin = (256, 256)

    def __init__(self, L1, L2, m1, m2, theta1, theta2, omega1, omega2, /, color=0x22DD22):
        self.L1 = L1
        self.L2 = L2
        self.m1 = m1
        self.m2 = m2
        self.theta1 = theta1
        self.theta2 = theta2
        self.omega1 = omega1
        self.omega2 = omega2
        self.color = color

        self.calculate_xy()

    @staticmethod
    def accel(L1, L2, m1, m2, theta1, theta2, omega1, omega2, g):
        num1 = (-g * (2 * m1 + m2) * math.sin(theta1)
                - m2 * g * math.sin(theta1 - 2 * theta2)
                - 2 * math.sin(theta1 - theta2) * m2 *
                (omega2**2 * L2 + omega1**2 * L1 * math.cos(theta1 - theta2)))
        den1 = L1 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2))
        a1 = num1 / den1

        num2 = (2 * math.sin(theta1 - theta2) *
            (omega1**2 * L1 * (m1 + m2)
                + g * (m1 + m2) * math.cos(theta1)
                + omega2**2 * L2 * m2 * math.cos(theta1 - theta2)))
        den2 = L2 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2))
        a2 = num2 / den2

        return a1, a2
    

    def calculate_xy(self):
        self.x1 = self.origin[0] + self.L1 * math.sin(self.theta1)
        self.y1 = self.origin[1] + self.L1 * math.cos(self.theta1)
        self.x2 = self.x1 + self.L2 * math.sin(self.theta2)
        self.y2 = self.y1 + self.L2 * math.cos(self.theta2)

    
    def step(self, n=1, path_surf=None):
        path_radius = 4

        for i in range(n):
            a1, a2 = self.accel(
                self.L1, self.L2, self.m1, self.m2,
                self.theta1, self.theta2, self.omega1, self.omega2, self.g
            )

            self.theta1 += self.omega1 * self.dt
            self.theta2 += self.omega2 * self.dt
            self.omega1 += a1 * self.dt
            self.omega2 += a2 * self.dt

            if path_surf is not None:
                if hasattr(self, "px2"):
                    pg.draw.line(path_surf, self.color,
                        (self.x2, self.y2), (self.px2, self.py2), path_radius
                    )
                self.px2 = self.x2
                self.py2 = self.y2
                self.calculate_xy()
        
        if path_surf is not None:
            path_surf.fill(0x060606, special_flags=pg.BLEND_ADD)


    def draw_sticks(self, surf):
        width = 2
        pg.draw.line(surf, 0xAAAAAA, self.origin, (self.x1, self.y1), width)
        pg.draw.line(surf, 0xAAAAAA, (self.x1, self.y1), (self.x2, self.y2), width)


    def draw_heads(self, surf, r):
        pg.draw.circle(surf, self.color, (self.x1, self.y1), r)
        pg.draw.circle(surf, self.color, (self.x2, self.y2), r)
