from matplotlib_example import *
from scipy.fftpack import fft

#Record a sound and plots the amplitude and spectrogram

SOUND=None


def play_audio(**kwargs):
    if SOUND:
        SOUND.play()
        return

def record_audio(view1,view2,*args,**kwargs):
    global SOUND
    snd_array=record_array(2.)
    SOUND=pg.sndarray.make_sound(snd_array)

    fig1 = pylab.figure(figsize=[4, 2], # Inches
                       dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                       )
    ax = fig1.gca()
    ax.plot(snd_array)
    make_fig(fig1,view1)

    fig2 = pylab.figure(figsize=[4, 2], # Inches
                       dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                       )
    spectrogram(fig2,snd_array[:,0])
    make_fig(fig2,view2)

def uinit(screen):
    ui=UI(screen)

    #Display element for the plot
    view1= ui.add('view',pos=(200,0),size=(400,200))
    view2= ui.add('view',pos=(200,200),size=(400,200))

    #Play button
    playbutton=ui.add('button',pos=(10,10),text='Play')
    playbutton.bind(play_audio)

    #Record button
    recordbutton=ui.add('button',pos=(60,10),text='Record')
    recordbutton.bind(record_audio,view1,view2)
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
