# -*- coding: utf-8 -*-

#1: INPUTS


import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))

alive=True

while alive:
    #Main loop

    events=pg.event.get() #Get all events caused by the user since last loop

    for e in events:

        print e

        #If the user presses the key "q", break the loop and end program
        if e.type==pg.KEYDOWN and e.unicode=='q':
            alive=False

