import PySimpleGUI as pg
import time
import sys
from pygame import mixer


# Section Popup
def win2m():
       
    lay2 = [[pg.T(f'', key='T')], [pg.OK()]]
    win2 = pg.Window('Popup', lay2, location=(250 ,0), no_titlebar=True)
    return win2

def sound():
    mixer.init()
    mixer.music.load("notification.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()


def main():
    # Color thingy
    pg.theme('dark amber')

    # Main Window
    layout = [[pg.Text('Timer = 0', key='timer', visible = False), pg.DropDown([(0.05, 0.05), (25, 5), (15, 2)], key='drop', )],
              [pg.B('CLOSE'), pg.B('START')]]
    win = pg.Window('Pomodoro', layout, location=(0,0), finalize=True, no_titlebar=True)
    

    while True:
        # Reads for events and values
        e, v = win.read()


        # Closes the program
        if e == pg.WINDOW_CLOSED or e == 'CLOSE':
            win.close()
            sys.exit()
        
        
        # Starts the counter upon pressing START
        if e == 'START':
            # Defines how long each section is 
            WORK_T, BREAK_T = v['drop']

            # Hides Elements
            win['drop'].update(visible = False)
            win['START'].hide_row()
            win['timer'].update(visible = True)
            
            # Start the counter at 0.00 and goes up to WORK_T
            M = 0
            T = time.time()
            while M < WORK_T:
                M = round((time.time() - T)/60, 2) 
                M = M + 0.00
                win['timer'].update(M)
                win.refresh()
            
            
            # Popup window to indicateb break time
            sound()
            if M >= WORK_T:
                win2 = win2m()
                win2.finalize()
                win2['T'].update(f'GOOD JOB!\nENJOY YOUR {BREAK_T} MINUTE BREAK NOW!')
                e2, v2 = win2.read()

                if e2 == pg.WINDOW_CLOSED or 'OK':
                    win2.close()
            
            # Start the counter at 0.00 and goes up to BREAK_T
            M = 0
            win['timer'].update(M)
            win.refresh()
            T = time.time()
            while M < BREAK_T:
                M = round((time.time() - T)/60, 2) 
                M = M + 0.00
                win['timer'].update(M)
                win.refresh()

                # Resets win to default
                if M >= BREAK_T:
                    sound()
                    win2 = win2m()
                    win2.finalize()
                    win2['T'].update(f'GOOD JOB!\nSECTION IS OVER.')
                    win2.refresh()
                    e2, v2 = win2.read()
                    
                    if e2 == pg.WINDOW_CLOSED or 'OK':
                        win2.close()

                    win['drop'].update(visible = True)
                    win['START'].unhide_row()
                    win['timer'].update(visible = False)
                    e, v = win.read()
            

if __name__ == '__main__':
    main()

main()