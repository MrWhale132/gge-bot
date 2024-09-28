import time

import pyautogui
import util
import common


def report_mouse_pos():
    pos = pyautogui.position()
    print(f"{pos[0]}, {pos[1]}")
    
if __name__ == '__main__':
    while True:
        report_mouse_pos()
        pyautogui.sleep(1)  # wait for 1 second before reporting the new position




from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")

def detect_mouse_clicks():
    # Set up a listener that runs `on_click` whenever the mouse is clicked
    with Listener(on_click=on_click) as listener:
        listener.join()

