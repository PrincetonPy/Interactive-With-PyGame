import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pygame as pg
import pylab
import numpy as np, numpy.random as rnd
from math import *

from ui_example import *
from snd_example import *

def make_fig(fig,view):
    #Interface with matplotlib, draw plot on a given UI_Item "view"

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()

    #Create pygame surface from string
    surf = pg.image.fromstring(raw_data, size, "RGB")

    #Set that surface as the default image of view
    view.images['idle']=surf
    view.update_sprite()
    pylab.close(fig)


def hist_example(view,nb=100,ui=None):
    '''Draw a histogram of random numbers between 0 and 1'''
    try:
        nb=nb()
    except:
        pass
    fig = pylab.figure(figsize=[4, 4], # Inches
                       dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                       )
    ax = fig.gca()
    ax.hist([rnd.random() for x in range(nb)])
    make_fig(fig,view)


def plot_example(view,puls=1,ui=None):
    '''Draw a histogram of random numbers between 0 and 1'''
    try:
        puls=puls()
    except:
        pass
    fig = pylab.figure(figsize=[4, 4], # Inches
                       dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                       )
    ax = fig.gca()
    ax.plot([2*pi*x/100. for x in range(100)],[sin(puls*2*pi*x/100.) for x in range(100)])
    make_fig(fig,view)

def play_audio(view,harmonic=1,**kwargs):
    #Play a sound that is an harmonic of A3 (220Hz)
    try:
        harmonic=harmonic()
    except:
        pass
    snd=make_sound(2.,harmonic*220)
    snd.play()

def uinit(screen):
    ui=UI(screen)

    #Counter: Harmonic
    view= ui.add('view',pos=(10,80),size=(100,20),text='Harmonic:')
    counter= ui.add('counter',pos=(10,100),size=(40,40))
    counter.set_val(1)

    #Display element for the plot
    view= ui.add('view',pos=(200,0),size=(400,400))
    view.bind(view.clean)

    #When the counter changes, call plot_example on the view
    counter.bind(plot_example,view,counter.get_val)
    plot_example(view,counter.get_val) #Do it with the initial value

    #Buttons for incrementing counter
    plus=ui.add('button',pos=(10,150),text='+')
    plus.bind(counter.increment,1)

    minus=ui.add('button',pos=(10,200),text='-')
    minus.bind(counter.increment,-1)

    #Play button
    playbutton=ui.add('button',pos=(10,10),text='Play')
    playbutton.bind(play_audio,view,counter.get_val)

    return ui

def main():
    pg.init()
    screen = pg.display.set_mode((600, 400), pg.DOUBLEBUF)
    ui=uinit(screen)

    alive=True
    while alive:
        draw(ui)
        alive=logic(ui)
    pg.display.quit()
    pg.quit()

if __name__ in '__main__':
    main()
