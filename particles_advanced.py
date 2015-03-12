# -*- coding: utf-8 -*-

#PARTICLES - FUN EXAMPLE

import pygame as pg
import numpy as np
from math import *

pg.init()
screen = pg.display.set_mode((640, 480), pg.DOUBLEBUF)
screen_rect=screen.get_rect()

import pyaudio
audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=88200,
                    input=True,
                    frames_per_buffer=50,
                    start=False)



##========================================================================#
##              PHYSICS
##========================================================================#

#Global constants

centralpower=1.5
gravconstant=0
use_pairwise=0
use_vortex=0

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

def gravity(pos,vel):
    #Constant directional acceleration
    return (0.,gravconstant)

def vortex(pos,vel):
    #Constant rotational acceleration around center of mass
    if not use_vortex:
        return 0
    return 2.*centralforce(pos,np.mean(pos,0),2.6,1)

def pairwise(pos,vel,use=0):
    #Pairwise attraction
    if not use_pairwise:
        return 0.
    #Exponent
    expo=centralpower
    if expo<1.:
        expo=1
    #Relative distance
    tmp=np.exp(pos)
    mat=np.log(np.outer(tmp,1./tmp ))
    return -2.*np.sum(mat*np.abs(mat)**(expo-1),1).reshape(pos.shape)/pos.shape[0]

def alignment(pos,vel,use=0):
    #Pairwise attraction+alignment
    if not use_pairwise:
        return 0.
    expo=centralpower
    if expo<1.:
        expo=1
    #Distance
    tmp=np.exp(pos)
    mat=np.log(np.outer(tmp,1./tmp ))
    #Aignment
    tmp=np.exp(vel)
    matvel=np.log(np.outer(tmp,1./tmp ))
    align=-.9*np.sum(matvel/(1.+np.abs(mat)),1).reshape(pos.shape)/pos.shape[0]
    attract=-2.*np.sum(mat*np.abs(mat)**(expo-1),1).reshape(pos.shape)/pos.shape[0]
    #repuls=2.*np.sum(mat/(1.+np.abs(mat)/.2)**(6),1).reshape(pos.shape)/pos.shape[0]
    return align+attract#+repuls

def centeratt(pos,vel):
    #Attraction to the center of gravity of others (cheap alterntative to pairwise)
    if use_pairwise:
        return 0.
    return -1.*centralforce(pos,np.mean(pos,0),centralpower)

##========================================================================#
##              DISPLAY
##========================================================================#

class Particle(pg.sprite.Sprite):
    mass=0.8
    pos=None
    vel=None
    acc=None
    color=((0,25,250),(255,140,40))
    size=(8,2)

    def create(self,pos=(0,0)):
        #Initialize a particle at given position
        self.pos=np.array(pos,dtype='float')
        self.vel=np.array((0.,0.))
        self.acc=np.array((0.,0.))
        self.color=np.array(self.color,dtype="int")

        #Create various colors and store them in self.images
        #(Allows to change the color of the particle
        self.images=[]
        for s in range(10):
            surf=pg.surface.Surface(self.size,pg.SRCALPHA)
            f=(s+2.)/12.
            surf.fill(self.color[1]*f + self.color[0]*(1-f) )
            self.images.append(surf)
        self.colorindex=0
        self.image=surf
        self.rect=surf.get_rect()
        self.rect.center=(self.pos*screen_rect.size).astype('int') #positions need to be integer

    def paint(self):
        #Select the color among skins (as imposed by ParticleCommander)
        l=len(self.images)
        self.image=self.images[int(min(l-1,self.colorindex*l)) ]
        #Rotate the image to show current direction
        angle=-atan2(*self.vel[::-1]/sum(self.vel))*360./2/pi
        self.image=pg.transform.rotate(self.image.copy(),angle)

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
            part.colorindex=hypot(*part.acc)**1.4

            #Reflection on walls
            if pos[0]<=0. or pos[0]>=1.:
                vel[0]*=-1
            if pos[1]<=0. or pos[1]>=1.:
                vel[1]*=-1
            part.pos=np.clip(pos,0.01,.99)

            #Update Rect
            part.rect.center=(part.pos*screen_rect.size).astype('int')

            #Update visuals of particle
            part.paint()

    def shock(self,magn=1.):
        for part in self.sprites():
            part.vel+=np.random.uniform(-.5,.5,2)*magn


def init():
    #Create particles and forces

    partsys=ParticleCommander()

    for i in range(200):
        p=Particle()
        p.create((0.5,0.5))
        partsys.add(p)

    #Add forces from particles_forces.py
    partsys.forces.append(mouseflee)
    partsys.forces.append(randforce)
    partsys.forces.append(friction)
    #partsys.forces.append(centeratt)
    partsys.forces.append(gravity)
    #partsys.forces.append(pairwise)
    partsys.forces.append(alignment)
    partsys.forces.append(vortex )


    return partsys


particles=init()

#Create event of type 30 every 40 milliseconds
#(30 is an event type unused by pygame. I use it as the signal for the physics simulation)
pg.time.set_timer(30,40) #Physics timer
pg.time.set_timer(29,80) #Sound timer


SHOCK_TIMER=-1

def main():
    alive=True
    global centralpower
    global mousepos
    global gravconstant
    global use_pairwise
    global use_vortex
    global SHOCK_TIMER

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

                if e.unicode=='g':
                    print "Toggle gravity"
                    if gravconstant:
                        gravconstant=0
                    else:
                        gravconstant=.1

                if e.unicode=='p':
                    print "Toggle pairwise"
                    if use_pairwise:
                        use_pairwise=0
                    else:
                        use_pairwise=.1

                if e.unicode=='v':
                    print "Toggle vortex"
                    if use_vortex:
                        use_vortex=0
                    else:
                        use_vortex=1

                if e.unicode=='s':
                    print "Toggle shock"
                    if SHOCK_TIMER>=0:
                        SHOCK_TIMER=-1
                    else:
                        SHOCK_TIMER=2

            if e.type==pg.MOUSEBUTTONDOWN:
                if e.button==4:
                    centralpower+=.1
                if e.button==5:
                    centralpower-=.1
                print 'Exponent of attraction to center:', centralpower

            if e.type==30:
                #Update physics
                particles.physics(0.04)

            if e.type==29 and SHOCK_TIMER>=0:
                #Update sound
                if SHOCK_TIMER>0:
                    SHOCK_TIMER-=1
                else:
                    stream.start_stream()

                    arr= np.fromstring(stream.read(50), dtype=np.int16)
                    #print np.max(arr)
                    if np.max(arr)>2000:
                        particles.shock(3. )
                        SHOCK_TIMER=12
                    stream.stop_stream()
                    #stream.close()

        screen.fill( np.clip(np.array((0,100,155))*(centralpower/10.),0,255) )

        particles.draw(screen)
        pg.display.flip()

main()
