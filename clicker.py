import keyboard
import pyautogui
import threading
import os
import json
from time import sleep

on = False
file_name = ''


mousepos = []
mouse_button = 'left'
delay = 0.005 # IN SECONDS





# CLICK THREAD
def click():
    while True:
        while on:
            if mousepos:
                for pos in mousepos:
                    pyautogui.moveTo(pos[0], pos[1])
                    pyautogui.click(button=mouse_button)
                    sleep(delay)
            else:
                pyautogui.click(button=mouse_button)
                sleep(delay)






# TOGGLES CLICKER ON AND OFF
def toggle():
    global on
    on = not on
    output()







# MOUSE POSITION
def getpos():
    mousepos.append(pyautogui.position())
    output()





# SAVE TO JSON FILE
def save():
    save_dict = {'mouse_button': mouse_button,
                'delay': delay,
                'mousepos': mousepos}
    with open(file_name, 'w') as file:
        json.dump(save_dict, file)


# LOAD FROM JSON FILE
def load():
    global mouse_button
    global delay
    global mousepos
    with open(file_name, 'r') as file:
        load_dict = json.load(file)
    mouse_button = load_dict['mouse_button']
    delay = load_dict['delay']
    mousepos = load_dict['mousepos']






# PRINTS MAIN MESSAGE
def output():
    os.system('cls')
    print('MOUSE CLICKER INFO')
    print(f'file                   {file_name}') if file_name else print('file                   none')
    print('status                 on') if on else print('status                 off')
    print(f'mouse button           {mouse_button}')
    print(f'delay                  {delay} seconds')
    print(f'click spots            {mousepos}') if mousepos else print('click spots            none')
    print('\n\n')


    print('CONTROLS')
    print('backslash              starts and stops clicker')
    print('delete                 exits program')
    print('shift + 1              adds click spots at current mouse position')
    print('\n\n')

    print('COMMANDS')
    print('left                   change mouse button to left')
    print('right                  change mousee button to right')
    print('delay [number]         sets delay between clicks in seconds')
    print('remove [position]      removes mouse click spots at [position]')
    print('resetpos               resets all mouse click spots')
    print('save                   saves settings to current file')
    print('save [file name]       saves settings to [file name]')
    print('load [file name]       loads settings from [file name]')
    print('resetfile              resets the file that\'s saved to and loaded from')

    print('\n\n\n')
    print('AWAITING COMMANDS...')








output()

# INPUT PARSER / HANDLER
def command_handler():
    global mouse_button
    global mousepos
    global file_name

    while True:
        inp = input()
        inpsplit = inp.split()

        try:
            #basic
            if inp == 'left':
                mouse_button = 'left'

            elif inp == 'right':
                mouse_button = 'right'

            elif inpsplit[0] in ['delay', 'space', 'spacing', 'time']:
                global delay
                delay = float(inpsplit[1])


            # mouse positions
            if inpsplit[0] in ['remove', 'delete', 'del', 'rem', 'rm']:
                if inpsplit[1] in ['last', 'end']:
                    del mousepos[-1]
                else:
                    del mousepos[int(inpsplit[1])]

            elif inp in ['resetpos', 'clearpos', 'resetspot', 'clearspot']:
                mousepos = []


            # save/load
            elif inpsplit[0] == 'save':
                if len(inpsplit) == 2:
                    file_name = 'saves/' + inpsplit[1] + '.json'
                save()

            elif inpsplit[0] == 'load':
                file_name = 'saves/' + inpsplit[1] + '.json'
                load()

            elif inp in ['resetfile', 'clearfile']:
                file_name = ''

            output()

        except ValueError:
            print('ERROR: non-numerical value entered')
        except IndexError:
            print('ERROR: not enough arguments')





keyboard.add_hotkey('shift+1', getpos)
keyboard.add_hotkey('\\', toggle)
keyboard.add_hotkey('delete', os._exit, args=[1])

click_thread = threading.Thread(target=click)
click_thread.daemon = True
click_thread.start()

commands_thread = threading.Thread(target=command_handler)
commands_thread.daemon = True
commands_thread.start()

keyboard.wait()