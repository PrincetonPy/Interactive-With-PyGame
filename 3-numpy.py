# -*- coding: utf-8 -*-

#2: SURFACES - FILLING, LOADING, BLITTING


import pygame as pg
import numpy as np

pg.init()
screen = pg.display.set_mode((640, 480))

def paint(screen,mode=0):
    size=(640,480,3)  #X,Y,Color (RGB)
    array=np.zeros(size) #Initialize the array with zeros

    for i in range(size[0]):
        for j in range(size[1]):
            x,y=(i+.5)/size[0],(j+.5)/size[1]

            #Color channels must be comprised between 0 and 255 and integer
            if mode==0:
                #Normal mode
                color=(255*x,255*y,0 )
            else:
                #Psychedelic mode
                color=(255*x,255*y,255./(x**2+y**2) )

            array[i,j,:]=np.array(color,dtype='int')
    pg.surfarray.blit_array(screen,array)

paint(screen,0)

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

            if e.unicode=='p':
                print 'Psychedelic mode'
                paint(screen,1)


    #Renew the screen
    pg.display.flip()
