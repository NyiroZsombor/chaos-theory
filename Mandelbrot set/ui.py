import pygame as pg

class UI:

    def __init__(self, size_x: int, size_y: int, mb_s):
        self.size_x = size_x
        self.size_y = size_y
        self.mb_s = mb_s
        self.display_coords: bool = False
        self.display_overlay: bool = False
        self.mouse_x: int = None
        self.mouse_y: int = None
        self.surface: pg.Surface= pg.Surface((self.size_x, self.size_y))
        self.font: pg.font.Font = pg.font.Font(size=24)
    
    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEMOTION:
            self.mouse_x, self.mouse_y = event.pos

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = UI.transform_point(self.mb_s, event.pos[0], event.pos[1])
            print("\tx", pos[0])
            print("\ty", pos[1])


    def render(self):
        self.surface.blit(self.mb_s.surface, (0, 0))

        if self.display_coords:
            x, y = UI.transform_point(self.mb_s, self.mouse_x, self.mouse_y)
            text: pg.Surface = self.font.render(
                f"({x}, {y})", False, (255, 255, 255)
            )

            self.surface.blit(text, (0, 0))

        if self.display_overlay:
            for i in range(2):
                if i == 0:
                    color: tuple[int] = self.mb_s.accent_color 
                else:
                    color: tuple[int] = self.mb_s.background_color

                start1: tuple[int] = (0, self.size_y // 2 + i)
                end1: tuple[int] = (self.size_x, self.size_y // 2 + i)

                start2: tuple[int] = (self.size_x // 2 + i, 0)
                end2: tuple[int] = (self.size_x // 2 + i, self.size_y)

                pg.draw.line(self.surface, color, start1, end1)
                pg.draw.line(self.surface, color, start2, end2)

    
    def transform_point(mb_s, x: float, y: float) -> tuple[float]:
        x: float = (x - mb_s.size_x / 2) * mb_s.scale_x + mb_s.offset_x
        y: float = (y - mb_s.size_y / 2) * mb_s.scale_y + mb_s.offset_y

        return (x, y)
