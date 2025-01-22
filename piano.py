import keyboard
from playsound import playsound # version 1.2.2
from os.path import dirname
import concurrent.futures

ERASE_CODE = "\033[2J"
RETURN_CODE = "\033[H"
DISPLAY = RETURN_CODE + '''Terminal Keys: press 'q' to quit
_____________________________________
|█| || |█|█| || || |█|█| || |█|█| |█|
|█| || |█|█| || || |█|█| || |█|█| |█|
|█|_||_|█|█|_||_||_|█|█|_||_|█|█|_|█|
|██|██|██|██|██|██|██|██|██|██|██|██|
|██|██|██|██|██|██|██|██|██|██|██|██|'''
#/\^/\^/\ /\^/\^/\^/\ /\^/\^/\ /\^
keyboard_list = list("a w s e d f t g y h u j k o l p ; ' ] enter".split())
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
    print(msg)

def main():

    run_program = True
    keys_pressed = set()
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=16)

    while run_program:

        print(DISPLAY)
        draw_played_notes(keys_pressed, pool)

        # COMMANDS
        if keyboard.is_pressed("q"):
            run_program = False
    
    pool.shutdown(wait=False)

if __name__ == "__main__":
    main()
    