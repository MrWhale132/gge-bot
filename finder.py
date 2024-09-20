import resources.ids as gui
from config import Config

import cv2
import pyautogui
import mss
import numpy as np

from util import *



matches=find(gui.fortress)

filtered=[]
# filter out duplicates
# i will be -1 first but its okay
for i in range(0, len(matches)):
    distance= (matches[i][0] - matches[i-1][0])**2 + (matches[i][1] - matches[i-1][1])**2
    # print(distance)
    if distance > 1000:
        filtered.append(matches[i])


print(len(matches))
print(len(filtered))

if len(filtered) == 0:
    print("No fortress found")
    exit()


pos=pyautogui.position()
filtered.insert(0, (pos[0], pos[1]))

# exit()
print("waiting")
import time
time.sleep(0.1)



fortress_display_offset_x = 50
fortress_display_offset_y = 50

fortress_lvl_offset_x = 85
fortress_lvl_offset_y = -23
fortress_lvl_width = 35
fortress_lvl_height = 25


for i in range(len(filtered)-1):
    target_x = filtered[i+1][0]
    target_y = filtered[i+1][1]

    fortress =(
        target_x + fortress_display_offset_x,
        target_y + fortress_display_offset_y)
    
    move_mouse_curve(filtered[i], fortress, lambda x: x**3, duration=1, steps=10)
    pyautogui.sleep(0.1)

    # lvl
    lvl_section=(
        target_x + fortress_lvl_offset_x,
        target_y + fortress_lvl_offset_y,
        fortress_lvl_width,
        fortress_lvl_height)
    
    section = getSection(lvl_section)
    lvl_img = screenshot(section=section, gray=True)
    
    #TODO Debug lvl
    # cv2.imshow("Fortress lvl", lvl_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    lvl_text=read(lvl_img)
    print(lvl_text)
    
    try:
        lvl = int(lvl_text)
    except ValueError:
        print("Fortress level is not a number")
        continue
    
    #TODO 50 for testing
    if lvl < 50:
        continue
    
    pyautogui.click()
    
    
    # select attack
    attack_offset_x = 150
    attack_offset_y = 30
    
    attack_option=(
        fortress[0] + attack_offset_x,
        fortress[1] + attack_offset_y)
    
    move_mouse_curve(fortress, attack_option, lambda x: x**3, duration=1, steps=10)
    
    pyautogui.click()
    
    
    # confirm
    confirm_x=1435
    confirm_y=925
    
    confirm_button=(
        confirm_x,
        confirm_y)
    
    move_mouse_curve(attack_option, confirm_button, lambda x: x**3, duration=1, steps=10)
    
    pyautogui.click()
    pyautogui.sleep(1)
    
    
    # show units
    matches= find(gui.unit_slot)
    # print(len(matches))
    #TODO hardcoded
    unit_slot_button=(
        matches[0][0]+20,
        matches[0][1]+20
    )
    
    move_mouse_curve(confirm_button, unit_slot_button, lambda x: x**3, duration=1, steps=10)
    
    pyautogui.click()
    pyautogui.sleep(0.1)
    # unit qty check
    first_unit_qty_x=850
    first_unit_qty_y=340
    unit_qty_box_width=35
    unit_qty_box_height=25
    
    unit_qty_section=(
        first_unit_qty_x, first_unit_qty_y,
        unit_qty_box_width,
        unit_qty_box_height)
    
    unit_qty_section = getSection(unit_qty_section)
    unit_qty_img=screenshot(section=unit_qty_section)
    
    #TODO Debug
    cv2.imshow("Unit qty", unit_qty_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    break



exit()
