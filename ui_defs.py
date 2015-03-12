import pygame as pg
import numpy as np


# CLASS DEFINITIONS FOR UI

class UI():
    fontsize=14
    def __init__(self,screen):
        self.screen=screen

        #Group of sprites
        self.group=pg.sprite.Group()

        #List of UI elements currently under the mouse
        self.hovering=[]

        #Dictionary associating each element with a function
        self.command={}

        #To write text, we need a pygame Font object, see function write below
        self.font=pg.font.Font(pg.font.get_default_font(),self.fontsize)

    def test_hover(self,pos):
        #Check which elements of the UI are currently under the mouse
        hover=[]
        for item in self.group:
            if item.rect.collidepoint(pos):
                hover.append(item)

        for item in hover:
            if not item in self.hovering:
                item.mouse_enter()

        for item in self.hovering:
            if not item in hover:
                item.mouse_leave()
            else:
                item.mouse_move()

        self.hovering=hover

    def mouse_press(self,pos):
        self.test_hover(pos)
        for item in self.hovering:
            item.mouse_press()

    def mouse_release(self,pos):
        self.test_hover(pos)
        for item in self.hovering:
            item.mouse_release()

    def add(self,typ,**kwargs):
        #Add a new element to the UI
        pos=kwargs.get('pos',(0,0))
        if typ=='button':
            item=Button(self)
        if typ=='view':
            item=View(self)
        if typ=='counter':
            item=Counter(self)
        size=kwargs.pop('size',(50,50))
        if 'text' in kwargs:
            item.text=kwargs['text']
        item.create_sprite(size,**kwargs)
        self.group.add(item)
        item.rect.topleft=pos
        return item

    def draw(self):
        self.group.draw(self.screen)

    def execute_command(self,item):
        #If a function has been bound to an item, execute it
        if item in self.command and self.command[item]:
            command,args,kwargs=self.command[item]
            kwargs['ui']=self
            command(*args,**kwargs)

    def write(self,text,surface):
        #Utility function for writing text on a surface
        txtimg=self.font.render(text,1,(255,255,255) )
        rect=txtimg.get_rect()
        srect=surface.get_rect()
        surface.blit(txtimg,np.array(srect.center)-rect.center )


class UI_Item(pg.sprite.Sprite):
    states={'hover':False,'click':False} #Possible states of the element
    priority=('click','hover') #Order in which states are checked to select image
    text=''

    def __init__(self,ui):
        pg.sprite.Sprite.__init__(self)
        self.images={} #Images associated with each state of the element
        self.master=ui #The element knows to which UI it belongs

    def mouse_enter(self):
        self.states['hover']=True
        self.update_sprite()

    def mouse_move(self):
        #When the mouse moves *within* the element
        pass

    def mouse_leave(self):
        self.states['hover']=False
        self.update_sprite()

    def mouse_press(self):
        self.states['click']=True
        self.update_sprite()

    def mouse_release(self):
        self.states['click']=False
        self.update_sprite()

    def update_sprite(self):
        #Check which image should be shown depending on current state
        for p in self.priority:
            if self.states[p] and p in self.images:
                self.image=self.images[p]
                return
        #If no state with a special image is activated, use the 'idle' image
        self.image=self.images['idle']

    def create_sprite(self,size,**kwargs):
        #Create images for states, by default only 'idle'
        surface=pg.surface.Surface( size )
        surface.fill( (0,0,0))
        self.master.write(self.text,surface)
        self.image=self.images['idle']=surface
        self.rect=pg.rect.Rect(kwargs.get('pos',(0,0)),size)


    def bind(self,command,*args,**kwargs):
        #Attach a function to this element, along with its arguments
        self.master.command[self]=(command,args,kwargs)

    def clean(self,*args,**kwargs):
        #Quick clean up of the image
        self.image.fill((0,0,0))

class Button(UI_Item):
    #Clickable UI Item

    def create_sprite(self,size,**kwargs):

        surface=pg.transform.smoothscale(pg.image.load('data/ball.png'),size)
        self.master.write(self.text,surface)
        self.images['idle']=surface.copy()

        surface.fill( (30,40,20),special_flags=pg.BLEND_ADD)
        self.images['hover']=surface.copy()

        surface.fill( (30,30,60),special_flags=pg.BLEND_ADD)
        self.images['click']=surface.copy()

        self.image=self.images['idle']
        self.rect=pg.rect.Rect((0,0),size)

    def mouse_release(self):
        UI_Item.mouse_release(self)
        self.master.execute_command(self)


class View(UI_Item):
    #Basic active UI Item

    def mouse_release(self):
        #Execute a command after you click on it
        UI_Item.mouse_release(self)
        self.master.execute_command(self)


class Counter(View):
    #UI Item that displays a number

    val=0
    vmin=1
    vmax=1000

    @property
    def text(self):
        return str(self.val)

    def set_val(self,v,**kwargs):
        if v<self.vmin or  v>self.vmax:
            return
        if self.val!=v:
            self.val=v
            self.create_sprite(self.rect.size,pos=self.rect.topleft)
            self.master.execute_command(self)

    def get_val(self,**kwargs):
        return self.val

    def increment(self,inc,**kwargs):
        self.set_val(self.val+inc)