# -*- coding: utf-8 -*-

#4: RECT, SPRITE AND GROUP

import pygame as pg
import numpy as np

pg.init()
screen = pg.display.set_mode((640, 480))



position=(0,0)
image=pg.image.load('data/ball.png')
image2=pg.image.load('data/ball2.png')


# A pygame.Rect is an object that is convenient
# for dealing with 2d surfaces
rect= image.get_rect() #Rectangle created from the ball image

print "Size of the image:", rect.size
print "Center of the image:", rect.center
print "Top-right corner of the image:", rect.topright
if  rect.collidepoint( (21,7)):
    print "The image contains the point (21,7)",

def create_balls(screen):
    #Instead of blitting images, we can draw them as groups of sprites

    group=pg.sprite.Group() #A group of sprites

    for i in range(10):
        #A sprite, which has two attributes:
        #.image, which is a surface
        #.rect, whose top-left corner and size gives the sprite position and size
        sprite=pg.sprite.Sprite()
        sprite.image=image.copy()
        sprite.rect=sprite.image.get_rect() #Create the rect from the image

        #Put all the balls at the center of the screen
        sprite.rect.center=screen.get_rect().center

        #Add the sprites to the group
        group.add(sprite)
    return group

def move_ball(group):
    for sprite in group:
        #Create a 2-vector of integers comprised between -1 and 1
        displacement=np.random.random_integers(-1,1,2)

        #Move the sprite by that vector
        sprite.rect.center+= displacement


def touch_ball(group):
    #Change the ball image if the mouse lays over it
    mousepos=pg.mouse.get_pos()
    for sprite in group:
        if sprite.rect.collidepoint(mousepos):
            sprite.image=image2
        else:
            sprite.image=image

group=create_balls(screen)

alive=True
while alive:
    events=pg.event.get()
    for e in events:
        if e.type==pg.KEYDOWN:
            if  e.unicode:
                print "KEY PRESSED:", e.unicode

            if e.unicode=='q':
                print "Quit"
                alive=False

    move_ball(group)
    touch_ball(group)


    screen.fill( (0,0,0))

    #Draw all the sprites in group on screen, at the positions given by their rects
    group.draw(screen)

    pg.display.flip()
