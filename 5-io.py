# -*- coding: utf-8 -*-

#5: INPUTS AND OUTPUTS - CAMERA, JOYSTICK AND SOUND

import pygame as pg
from pygame import camera
import numpy as np
from math import *
from snd_example import *
from pygame import joystick

pg.init()
SCREENSIZE = [640, 480]
screen = pg.display.set_mode(SCREENSIZE, pg.DOUBLEBUF)


# Initialize camera
camera.init()
cam = camera.Camera('/dev/video0', SCREENSIZE) #Change /dev/video0 to wherever your webcam is
cam.start()

#Initialize joystick
joystick.init()
joy=joystick.Joystick(0)
joy.init()

#Load a sound
ksnd=pg.mixer.Sound("data/k.ogg")

#Load sounds into an array
snds=[pg.mixer.Sound("data/ch{}.wav".format(i+1)) for i in range(5)]

#This surface will be used to superimpose effects on the webcam image
veil=pg.surface.Surface(SCREENSIZE)
veil.fill((255,255,255))
veil.set_alpha(0)

#Create event of type 30 every 30 milliseconds
#(30 is an event type unused by pygame)
pg.time.set_timer(30,40)

alive=True
i=0
while alive:
    camimage = cam.get_image()  # Get current webcam image
    screen.fill([0, 0, 0])  # Blank fill the screen
    screen.blit(camimage, (0, 0))  # Load new image on screen
    for e in pg.event.get():
        if e.type==pg.QUIT:
            alive=False

        if e.type==pg.MOUSEBUTTONDOWN:
            snd=make_sound(3,(i+1)*220.)
            snd.play()
            i+=1
            i=i%4
        if e.type == pg.JOYBUTTONDOWN:
            if e.button==2:
                veil.fill( (0,0,255) )
                veil.set_alpha(200)
            if e.button==3:
                veil.fill( (255,255,0) )
                veil.set_alpha(200)
            if e.button==1:
                veil.fill( (255,0,0) )
                veil.set_alpha(200)
            if e.button==0:
                veil.fill( (0,255,0) )
                veil.set_alpha(200)
            if e.button==4:
                veil.fill( (255,125,0) )
                veil.set_alpha(200)
            if e.button<len(snds):
                snds[e.button].play(maxtime=1000) #Limit the duration of the sound


        if e.type == pg.JOYHATMOTION and e.value[1]:
            color=np.array((255,255,255))*abs(e.value[1])*.1
            ksnd.play()
            veil.fill( color)
            veil.set_alpha(200)

        if e.type==pg.KEYDOWN:
            if e.unicode=='q':
                alive=False


        if e.type==30:
            veil_alpha=veil.get_alpha()
            if veil_alpha>0:
                veil.set_alpha(veil_alpha-50)
    screen.blit(veil,(0,0))
    pg.display.flip()
