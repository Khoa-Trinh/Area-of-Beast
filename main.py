import pygame as py
import settings as st
import sys

py.init()

screen = py.display.set_mode((st., py.RESIZABLE)

running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    screen.fill(("red"))
    py.display.flip()
py.clock.tick(60)
py.quit()     