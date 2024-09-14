import pyautogui

def report_mouse_pos():
    pos = pyautogui.position()
    print(f"{pos[0]}, {pos[1]}")
    
if __name__ == '__main__':
    while True:
        report_mouse_pos()
        pyautogui.sleep(1)  # wait for 1 second before reporting the new position