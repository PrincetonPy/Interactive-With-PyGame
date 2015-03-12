# -*- coding: utf-8 -*-

#SURFACES - BLENDING


import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))


alive=True

position=(0,0)
image=pg.image.load('refimg.jpg')

while alive:
    events=pg.event.get()
    for e in events:
        if e.type==pg.KEYDOWN:
            if  e.unicode:
                print "KEY PRESSED:", e.unicode

            if e.unicode=='q':
                print "Quit"
                alive=False

            if e.unicode=='f':
                print "Fill the screen"
                screen.fill( (255,0,0))

            if e.unicode=='p':
                print "Paste image"
                screen.blit(image,position)

            if e.unicode=='a':
                print "Blend image: ADD"
                screen.blit(image,position,special_flags=pg.BLEND_ADD)

            if e.unicode=='m':
                print "Blend image: MULTIPLY"
                screen.blit(image,position,special_flags=pg.BLEND_MULT)

            if e.unicode=='b':
                print "Blit image 2 on image 1"
                image2=pg.image.load('refimg2.png')
                image.blit(image2,(94,90))
                screen.blit(image,position)

            if e.unicode=='l':
                print "Reload original image"
                image=pg.image.load('refimg.jpg')
                screen.blit(image,position)

    pg.display.flip()
