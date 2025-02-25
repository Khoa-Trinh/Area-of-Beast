import pygame as py
import sys

py.init()

screen = py.display.set_mode((800, 800), py.RESIZABLE)

running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.fill(("red"))
    screen.draw.polygon(screen, "magenta", )
    py.display.flip()
py.clock.tick(60)
py.quit()     