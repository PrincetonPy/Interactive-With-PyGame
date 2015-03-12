import pygame as pg

from ui_defs import *

# SILLY UI EXAMPLE: CLICK ON THE BUTTON AND IT JUMPS

def logic(ui):
    #Basic function for relaying pygame events to UI
    #Returns "alive" for the main loop
    events=pg.event.get()
    for e in events:
        if e.type==pg.QUIT:
            return False

        if e.type==pg.MOUSEMOTION:
            #If the mouse moves, look which UI elements are under it
            ui.test_hover(e.pos)

        if e.type == pg.MOUSEBUTTONDOWN:
            #Relay click to UI elements
            ui.mouse_press(e.pos)

        if e.type == pg.MOUSEBUTTONUP:
            #Relay release to UI elements
            ui.mouse_release(e.pos)

    return True

def draw(ui):
    #Basic function for displaying UI
    ui.screen.fill((0,0,0))
    ui.draw()
    pg.display.flip()

def response(button,**kwargs):
    #When the button is pressed, it jumps to another location
    print "Pressed button!"
    button.rect.topleft=(np.random.randint(0,500),np.random.randint(0,300) )

def uinit(screen):
    #Create UI with one button
    ui=UI(screen)
    button=ui.add('button',pos=(10,10))
    button.bind(response,button)
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

