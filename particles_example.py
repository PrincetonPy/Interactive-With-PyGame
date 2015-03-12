# -*- coding: utf-8 -*-

#PARTICLES - MINIMAL EXAMPLE


import pygame as pg
import numpy as np
from math import *

pg.init()
screen = pg.display.set_mode((640, 480), pg.DOUBLEBUF)
screen_rect=screen.get_rect()

##========================================================================#
##              PHYSICS
##========================================================================#

#Definition of the forces that can act on particles

def centralforce(pos,ref,expo=2,vort=False):
    #Any kind of central attraction or repulsion
    dist=pos -ref
    if vort:#vortex force (acceleration orthogonal to relative pos)
        dist=np.cross(dist,(0,0,1))[:,:2]
    hyp=np.hypot(*dist.T).reshape(pos.shape[0],1)
    hyp[ hyp==0]=0.01
    force=dist*0.001/hyp**(expo+1)
    force=np.clip(force,-1.,1.)
    return force

def mouseflee(pos,vel):
    #Evade the mouse
    return  centralforce(pos,mousepos,2)

def randforce(pos,vel):
    #Thermal noise
    return 0.7*(np.random.random(pos.shape)-.5)

def friction(pos,vel):
    #Bounds possible velocities
    return -.5*vel

##========================================================================#
##              DISPLAY
##========================================================================#

class Particle(pg.sprite.Sprite):
    mass=0.8
    size=(2,2)

    def create(self,pos=(0.5,0.5)):
        #Initialize a particle at given position
        self.pos=np.array(pos,dtype='float')
        self.vel=np.array((0.,0.))
        self.acc=np.array((0.,0.))

        #Create image
        surf=pg.surface.Surface(self.size)
        surf.fill((255,255,255))
        self.image=surf

        #Create rect
        self.rect=surf.get_rect()
        self.rect.center=(self.pos*screen_rect.size).astype('int')


class ParticleCommander(pg.sprite.Group):
 #Group of particles+forces+equations of motion

    def __init__(self):
        pg.sprite.Group.__init__(self)
        self.forces=[]

    def calc_forces(self):
        #Sum of forces on one particle
        pos=np.array([part.pos for part in self.sprites()])
        vel=np.array([part.vel for part in self.sprites()])

        ftot=np.zeros(pos.shape)
        for f in self.forces:
            ftot+=f(pos,vel)
        return ftot

    def physics(self,deltat=1.):
        #Equations of motion
        forces=self.calc_forces()
        for i,part in enumerate(self.sprites()):
            pos,vel=part.pos,part.vel
            part.acc=forces[i]/part.mass
            vel+=deltat*part.acc
            pos+=deltat*vel

            #Reflection on walls
            if pos[0]<=0. or pos[0]>=1.:
                vel[0]*=-1
            if pos[1]<=0. or pos[1]>=1.:
                vel[1]*=-1
            part.pos=np.clip(pos,0.,1.)

            #Update Rect
            part.rect.center=(part.pos*screen_rect.size).astype('int')


def init():
    #Create particles and forces

    partsys=ParticleCommander()

    for i in range(2000):
        p=Particle()
        p.create((0.5,0.5))
        partsys.add(p)

    #Add forces from particles_forces.py
    partsys.forces+=[mouseflee,randforce,friction]

    return partsys



#Create event of type 30 every 40 milliseconds
#(30 is an event type unused by pygame. I use it as the signal for the physics simulation)
pg.time.set_timer(30,60) #Physics timer


def main():
    global mousepos
    particles=init()

    alive=True
    while alive:
        events=pg.event.get()
        mousepos=np.array(pg.mouse.get_pos(),dtype="float") /screen_rect.size
        for e in events:
            if e.type==pg.QUIT:
                alive=False

            if e.type==pg.KEYDOWN:
                if  e.unicode:
                    print "KEY PRESSED:", e.unicode

                if e.unicode=='q':
                    print "Quit"
                    alive=False

                if e.unicode=='r':
                    print "Reinitialize"
                    for p in particles.sprites():
                        p.create((0.5,0.5) )

            if e.type==30:
                #Update physics
                particles.physics(0.06)

        screen.fill( (0,20,20) )

        particles.draw(screen)
        pg.display.flip()

main()
