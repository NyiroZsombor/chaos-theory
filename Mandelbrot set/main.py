import pygame as pg
from .mandelbrot import MandelbrotSet
import sys
import threading

from .ui import UI

# TODO: interactive ui, measurements

def get_input() -> None:
    auto_render: bool = True
    mb_s.render()

    while True:
        if stop_event.is_set():
            print("exiting")
            sys.exit()

        command: str = input("# ").split()
        if len(command) == 0: continue

        try:
            if command[0] == "exit":
                stop_event.set()

            elif command[0] == "help":
                print("\thelp - display list and description of commands")
                print("\texit - exits the program")
                print("\tzoom <value> - set zoom to <value>")
                print("\tx <value> - set x position to <value>, " 
                    + "positive goes RIGHT")
                print("\ty <value> - set y position to <value>, "
                    + "positive goes DOWN")
                print("\tdepth <value> - set depth to <value>, default is 20")
                print("\tsave <value> - save image without any overlay or ui "
                    + "to images/<value>.png, <value> is optional")
                print("\tpos - toggle mouse position display in topleft")
                print("\toverlay - toggle vertical and horizontal "
                    + "lines in the center")
                print("\tauto-render - toggle automatic rendering after "
                    + "changing display properties (x, y, zoom, depth)")
                print("\trender - manually render the screen")
                print("\tcolor-acc <r> <g> <b> - sets the accent color")
                print("\tcolor-bg <r> <g> <b> - sets the background color")

            elif command[0] == "zoom":
                mb_s.set_zoom(float(command[1]))
                print(f"\tzoom is now {mb_s.zoom}")
                if auto_render: mb_s.render()

            elif command[0] == "x":
                mb_s.set_offset_x(float(command[1]))
                print(f"\tx position is now {mb_s.offset_x}")
                if auto_render: mb_s.render()
            
            elif command[0] == "y":
                mb_s.set_offset_y(float(command[1]))
                print(f"\ty position is now {mb_s.offset_y}")
                if auto_render: mb_s.render()

            elif command[0] == "depth":
                mb_s.set_depth(int(command[1]))
                print(f"\tdepth is now {mb_s.depth}")
                if auto_render: mb_s.render()

            elif command[0] == "save":
                name: str = f"({mb_s.offset_x}_{mb_s.offset_y})"
                name = f"{mb_s.zoom}x_{name}"
                if len(command) == 1:
                    name = name.replace(".", ",")
                    name += f"_{mb_s.depth}.png"
                    name = "images/" + name
                else:
                    name = command[1] + ".png"
                    name = "images/" + name

                pg.image.save(mb_s.surface, name)
                print(f"\timage saved to {name}")

            elif command[0] == "get":
                print(
                    f"\tx: {mb_s.offset_x}",
                    f"\ty: {mb_s.offset_y}",
                    f"\tzoom: {mb_s.zoom}",
                    f"\tdepth: {mb_s.depth}",
                    sep="\n")
                
            elif command[0] == "pos":
                ui.display_coords = not ui.display_coords
                print(f"\tpos is now {ui.display_coords}")

            elif command[0] == "overlay":
                ui.display_overlay = not ui.display_overlay
                print(f"\toverlay is now {ui.display_overlay}")

            elif command[0] == "auto-render":
                auto_render = not auto_render
                print(f"\tauto-render is now {auto_render}")

            elif command[0] == "render":
                mb_s.render()

            elif command[0] == "color-acc":
                mb_s.accent_color = tuple(map(lambda x: int(x), command[1:4]))
                print(f"\taccent color is now {mb_s.accent_color}")
                if auto_render: mb_s.render()

            elif command[0] == "color-bg":
                mb_s.background_color = tuple(map(lambda x: int(x), command[1:4]))
                print(f"\tbackground color is now {mb_s.background_color}")
                if auto_render: mb_s.render()

            else:
                print("invalid command")

        except Exception as e:
            print("invalid input: ", e)

pg.init()

size = (500, 500)
screen: pg.Surface = pg.display.set_mode(size)
mb_s = MandelbrotSet(*size)
ui: UI = UI(*size, mb_s)
screen.blit(mb_s.surface, (0, 0))

terminal_thread: threading.Thread = threading.Thread(target=get_input)
terminal_thread.start()
stop_event: threading.Event = threading.Event()

while True:
    if stop_event.is_set():
        print("press enter to exit the terminal ", end="")
        pg.quit()
        sys.exit()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            stop_event.set()

        ui.handle_events(event)

    ui.render()
    screen.blit(ui.surface, (0, 0))

    pg.display.flip()