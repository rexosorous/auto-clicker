import pynput
import threading
import os
import json
from time import sleep

on = False
mouse = pynput.mouse.Controller()
file_name = ''


mousepos = []
mouse_button = pynput.mouse.Button.left
delay = 0.005 # IN SECONDS





class exit(Exception):
    pass





# STOP THREAD
def stop(key):
    global on
    if key == pynput.keyboard.KeyCode(220):
        on = True if not on else False
    if key == pynput.keyboard.Key.delete:
        os._exit(1)



def listen():
    with pynput.keyboard.Listener(on_press=stop) as listener:
        listener.join()


stop_thread = threading.Thread(target=listen)
stop_thread.daemon = True
stop_thread.start()







# CLICK THREAD
def click():
    global mousepos
    while True:
        while on:
            if mousepos:
                for pos in mousepos:
                    mouse.move(pos[0] - mouse.position[0], pos[1] - mouse.position[1])
                    sleep(0.1)
                    mouse.press(mouse_button)
                    sleep(0.1)
                    mouse.release(mouse_button)
                    sleep(delay)
            else:
                mouse.press(mouse_button)
                mouse.release(mouse_button)
                sleep(delay)


click_thread = threading.Thread(target=click)
click_thread.daemon = True
click_thread.start()







# MOUSE POSITION THREAD
def getpos(x, y, button, pressed):
    global mousepos
    if button == pynput.mouse.Button.middle and pressed:
        mousepos.append(mouse.position)
        raise exit


def pos_listen():
    try:
        with pynput.mouse.Listener(on_click=getpos) as listener:
            listener.join()
    except exit:
        pass





def save():
    global file_name
    save_dict = {'mouse_button': 'left' if mouse_button == pynput.mouse.Button.left else 'right',
                'delay': delay,
                'mousepos': mousepos}
    with open(file_name, 'w') as file:
        json.dump(save_dict, file)



def load():
    global file_name
    with open(file_name, 'r') as file:
        load_dict = json.load(file)
    mouse_button = pynput.mouse.Button.left if load_dict['mouse_button'] == left else pynput.mouse.Button.right
    delay = load_dict['delay']
    mousepos = load_dict['mousepos']







def output():
    os.system('cls')
    print('MOUSE CLICKER INFO')
    print(f'file:         {file_name}') if file_name else print('file:         none')
    print('status:       on') if on else print('status:       off')
    print('mouse button: left') if mouse_button == pynput.mouse.Button.left else print('mouse button: right')
    print(f'delay:        {delay} seconds')
    print(f'click spots:  {mousepos}') if mousepos else print('click spots:  none')
    print('\n\n')

    print('CONTROLS')
    print('left                  change mouse button to left')
    print('right                 change mousee button to right')
    print('delay [number]        sets delay between clicks in seconds')
    print('add                   adds mouse spots to click at')
    print('remove [position]     removes mouse click spots at [position]')
    print('resetpos              resets all mouse click spots')
    print('save                  saves settings to current file')
    print('save [file name]      saves settings to [file name]')
    print('load [file name]      loads settings from [file name]')
    print('resetfile             resets the file that\'s saved to and loaded from')

    print('\n\n\n')
    print('AWAITING COMMANDS...')









# INPUTS
while True:
    inp = input()
    inpsplit = inp.split()

    try:
        if inp == 'left':
            mouse_button = pynput.mouse.Button.left
        elif inp == 'right':
            mouse_button = pynput.mouse.Button.right
        elif inpsplit[0] in ['delay', 'space', 'spacing', 'time']:
            delay = int(inpsplit[1])
        elif inp == 'add':
            print('press middle mouse button to get mouse position')
            pos_thread = threading.Thread(target=pos_listen)
            pos_thread.daemon = True
            pos_thread.start()
        elif inp in ['resetpos', 'clearpos', 'resetspot', 'clearspot']:
            mousepos = []
        elif inp[0] in ['remove', 'delete', 'del', 'rem', 'rm']:
            if inp[1] in ['last', 'end']:
                del mousepos[-1]
            else:
                del mousepos[int(inp[1])]
        elif inp[0] == 'save':
            if inp[1]:
                file_name = inp[1]
            save()
        elif inp[1] == 'load':
            file_name = inp[1]
            load()
        elif inp in ['resetfile', 'clearfile']:
            file_name = ''

        output()

    except ValueError:
        print('ERROR: non-numerical value entered')
    except IndexError:
        print('ERROR: not enough arguments')