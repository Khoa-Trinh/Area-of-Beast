import pygamefunction as pf
import pygame as py
import sys

py.init()

screen_width = 800
screen_height = 800
screen = py.display.set_mode((screen_width, screen_height), py.RESIZABLE)
py.display.set_caption("Beta Test")



running = True
while running:
    for e in py.e.get():
        if e.type == py.QUIT:
            running = False

py.quit()
py.time.Clock.tick(60)
sys.exit()