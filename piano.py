
import pygame.midi
import keyboard

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
note_points = [0,2,3,5]

red_code = "\033[31m"
reset_code = "\033[0m"

arrow_list = ["^","/\\"]
blank_list = [" ","  "]
    
print(ERASE_CODE)
def draw_played_notes(midi_output: pygame.midi.Output, keys_held: set):
    msg = " "
    for i in range(0,20):
        target_key = keyboard_list[i]
        pitch = i + 48
        if keyboard.is_pressed(target_key):
            if target_key not in keys_held:
                play_note(midi_output, pitch, 70)
                keys_held.add(target_key)
            draw_list = arrow_list
        else:
            play_note(midi_output, pitch, 0)
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

def setup_midi_output():
    pygame.midi.init()
    return pygame.midi.Output(pygame.midi.get_default_output_id())

def play_note(midi_output, pitch, velocity):
    if velocity > 0:
        midi_output.note_on(pitch, velocity)
    else:
        midi_output.note_off(pitch)


def main():

    midi_output = setup_midi_output()

    run_program = True
    keys_pressed = set()

    while run_program:

        print(DISPLAY)
        draw_played_notes(midi_output, keys_pressed)

        # COMMANDS
        if keyboard.is_pressed("q"):
            run_program = False

    midi_output.close()
    pygame.midi.quit()

if __name__ == "__main__":
    main()
    