import time

import pyautogui
import util
import common

# pyautogui.dragRel(0,-200,duration=1)
# exit()


from pynput import keyboard

def asPoint(pos):
    return f"Point({pos[0]}, {pos[1]}),"

def on_press(key):
    if key == keyboard.Key.space:
        print(asPoint(util.mousePos()))
    if key == keyboard.Key.esc:
        exit()


def listen():
    # Set up a listener that runs `on_click` whenever the mouse is clicked
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()




if __name__ == '__main__':
    listen()
    # while True:
    #     report_mouse_pos()
    #     pyautogui.sleep(1)  # wait for 1 second before reporting the new position

