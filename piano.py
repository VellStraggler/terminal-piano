from atexit import register
import signal
import keyboard
from playsound import playsound # version 1.2.2
from os.path import dirname
import os
import concurrent.futures
import sys
import termios
# to get rid of input the builds up after the program ends

ERASE_CODE = "\033[2J"
ERASE_DOWN_CODE = "\033[J"
TO_START_POINT = "\033[7;0H"
RETURN_CODE = "\033[H"
DISPLAY = RETURN_CODE + '''Terminal Keys: press 'q' to quit
_____________________________________
|█| || |█|█| || || |█|█| || |█|█| |█|
|█| || |█|█| || || |█|█| || |█|█| |█|
|█|_||_|█|█|_||_||_|█|█|_||_|█|█|_|█|
|██|██|██|██|██|██|██|██|██|██|██|██|
|██|██|██|██|██|██|██|██|██|██|██|██|'''
#/\^/\^/\ /\^/\^/\^/\ /\^/\^/\ /\^
keyboard_list = list("a w s e d f t g y h u j k o l p ; ' ] \\".split())
black_keys = [1, 3, 6, 8, 10]

arrow_list = ["^","/\\"]
blank_list = [" ","  "]

FILE_PREFIX = dirname(__file__) + "/notes/"
    
print(ERASE_CODE)
def draw_played_notes(keys_held: set, pool):
    msg = " "
    for i in range(0,20):
        target_key = keyboard_list[i]
        pitch = i
        if keyboard.is_pressed(target_key):
            if target_key not in keys_held:

                pool.submit(playsound, (FILE_PREFIX + str(pitch) + ".1.wav"))

                keys_held.add(target_key)
            draw_list = arrow_list
        else:
            if target_key in keys_held:
                keys_held.remove(target_key)
            draw_list = blank_list
        m = i%12
        if m in black_keys:
            msg += draw_list[0] # "^"
        else:
            msg += draw_list[1] # "/\\"
            if m in [4,11]:
                msg += " "
    print(msg + ERASE_DOWN_CODE + TO_START_POINT)

def main():

    run_program = True
    keys_pressed = set()
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=16)

    print(DISPLAY)
    # print display once, and bring cursor back to row below it
    while run_program:

        draw_played_notes(keys_pressed, pool)

        # COMMANDS
        if keyboard.is_pressed("q"):
            run_program = False
    
    pool.shutdown(wait=False)

    sys.stdout.write("\033[3J\033[H\033[2J")
    sys.stdout.flush()
    register(cleanup)

def cleanup():
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    main()
    