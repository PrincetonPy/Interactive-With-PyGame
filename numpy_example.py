# -*- coding: utf-8 -*-


# MANIPULATING PIXELS AS A NUMPY ARRAY

import pygame as pg
from math import *
import numpy as np, scipy.signal

pg.init()
screen = pg.display.set_mode((640, 480), pg.DOUBLEBUF)

def invert(image):
    #Invert colors

    #Create a numpy array that refers to the pixels of the image
    #It is a 3d array with dimensions: x, y, color
    img_array=pg.surfarray.pixels3d(image)

    #Take the complementary of the pixel values
    img_array[:,:]=255-img_array[:,:]


def make_gaussian_array(size):
    center=(size[0]/2.,size[1]/2.)
    sigma=min(size)/2.

    array=np.zeros(size)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            dist=(i-center[0])**2 + (j-center[1])**2
            array[i,j]=exp(-dist/(2*sigma**2))

    return array/np.sum(array)


def blur(image,s=6):
    #Create a numpy array that refers to the pixels of the image
    img_array=pg.surfarray.pixels3d(image)

    #Create a gaussian array
    gauss=make_gaussian_array((s,s))

    #For each color channel, convolve the image with the gaussian
    for c in range(3):
        img_array[:,:,c]=scipy.signal.convolve2d(img_array[:,:,c],gauss,mode='same')


def bloom(image):
    #Copy the image and keep only the high value pixels
    layer=image.copy()
    layer_array=pg.surfarray.pixels3d(layer)
    layer_array[layer_array<160]=0
    del layer_array #once the array is unneeded, delete it to unlock the surface

    #Blur the copy, then add it back to the original
    blur(layer,8)
    image.blit(layer,(0,0),special_flags=pg.BLEND_ADD)


alive=True
position=(0,0)
image=pg.image.load('data/refimg.jpg')

while alive:
    events=pg.event.get()
    for e in events:

        if e.type==pg.MOUSEMOTION:
            position=e.pos

        if e.type==pg.KEYDOWN:
            if  e.unicode:
                print "KEY PRESSED:", e.unicode

            if e.unicode=='q':
                print "Quit"
                alive=False

            if e.unicode=='b':
                print "blur"
                blur(image)

            if e.unicode=='i':
                print "invert"
                invert(image)

            if e.unicode=='m':
                print "bloom"
                bloom(image)

            if e.unicode=='l':
                print "reload"
                image=pg.image.load('data/refimg.jpg')
    screen.fill((0,0,0) )
    screen.blit(image,(0,0))
    pg.display.flip()
