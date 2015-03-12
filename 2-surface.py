# -*- coding: utf-8 -*-

#2: SURFACES - FILLING, LOADING, BLITTING


import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))

print screen.__class__
#The variable "screen" is a pygame Surface object
#that details the color of each pixel in the window.
#Its methods include fill and blit, see below.

def fill(screen):
    #Fills surface with red
    color=(255,0,0)
    screen.fill( color)

def load(screen,position):
    #Loads an external image and paste it on a suface at given position
    surface=pg.image.load('data/refimg.jpg') #Creates a surface from an external image
    screen.blit(surface,position) #Pastes "surface" on "screen" at position

alive=True

while alive:
    events=pg.event.get()
    for e in events:
        if e.type==pg.QUIT:
            #When the user closes the window
            alive=False

        if e.type==pg.KEYDOWN:
            if  e.unicode:
                print "KEY PRESSED:", e.unicode

            if e.unicode=='q':
                print "Quit"
                alive=False

            if e.unicode=='f':
                print "Fill the screen"
                fill(screen)

            if e.unicode=='l':
                print "Paste image"
                load(screen, (0,0) )

        if e.type==pg.MOUSEBUTTONDOWN:
            mouse_position=e.pos
            print "Paste image to",mouse_position
            load(screen,mouse_position)

    #Renew the screen
    pg.display.flip()
