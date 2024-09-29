from actions import attack_with_preset
from common import Presets
from util import Point

def main():
    #TODO comeback later when we have a more accurate image finder
    towers:list[Point]=[
        Point(1368,813),
        Point(1443,1354),
        Point(1060,970),
        Point(834,1200),
        Point(600,886),
        Point(520,580),
        Point(900,500),
        Point(990,120),
        Point(1370,200),
        Point(1450,510),
        Point(1835,360),
        Point(2135,435),
        Point(1985,740),
        Point(1905,1010), #they are outside of the screen
        Point(990,1310),
    ]
    from config import CommanderConfig
    blacklist=CommanderConfig.barbarian_tower_blacklist_commanders


    def attack(tower:Point):
        attack_with_preset(target=tower,preset=Presets.dragon_cultist,use_horses=True,commander_blacklist=blacklist,first_wave_only=True)


    attack(towers[0])

    for i in range(1,13):
        attack(towers[i])

    import pyautogui
    pyautogui.dragRel(0,-200,duration=1)

    for i in range(13,15):
        attack(towers[i])



import eventloop
eventloop.wrap(main)
exit()



















import time
import typing

import pynput.keyboard

import util
from models.objects.Point import Point
import pyautogui
from common import ActionPalette,AttackConfirmationPanel, AttackPanel, HorseSelectionMenu

from resources import ids as gui
worldmap = gui.dragon_cultist_free_npc_tower_level_3


def find():
    pyautogui.sleep(1)
    towers, screenshot = util.find(gui.dragon_cultist_free_npc_tower_level_3, returnScreenshot=True, threshold=0.80)
    print(len(towers))
    util.showMatches(towers, gui.dragon_cultist_free_npc_tower_level_3, screenshot)

def move_to():
    for tower_location in towers:
        tower_click_point_offset =Point(10, 10,relative=True)
        tower_middle_point = tower_location + tower_click_point_offset

        util.click(tower_middle_point)

        util.click(ActionPalette.attack_button_offset)

        util.click(AttackConfirmationPanel.confirm_button_point)
        #opening the attack menu can span multiple seconds
        #TODO add retry logic, while loop
        pyautogui.sleep(2)

        open_presets()
        select_preset()





def open_presets():
    util.click(AttackPanel.attack_preset_button_point)


from common import Presets

def select_preset():
    #TODO find the NPC preset with util.find
    # presets = util.screenshot(AttackPanel.attack_presets_dropdown_section)
    # util.showImg(presets)

    util.click(AttackPanel.nth_preset_button_point(Presets.dragon_cultist))
    util.click(AttackPanel.apply_selected_preset_to_first_wave_button_point)
    util.click(AttackPanel.launch_attack_button_point)
    util.click(HorseSelectionMenu.level_1_speed_boost_point)
    util.click(HorseSelectionMenu.confirm_button_point)

    # exit()


from thread import Thread

def loop():
    # print("init loop")
    # time.sleep(4)
    # print("finish loop")
    # return
    while True:
        print("loop")
        # pyautogui.dragRel(0,500,0.5 )
        time.sleep(1)

import eventloop

eventloop.wrap(loop)
print("finisged")
exit()


from pynput import keyboard


def listen(key):
    if (key == keyboard.Key.esc) or (key == keyboard.Key.space) :
        t.kill()
        print("killed t")
    else:
        if isinstance(key,pynput.keyboard.KeyCode):print(key.char)
        if isinstance(key, pynput.keyboard.Key):print(key.value)


t = Thread(loop)
print("started t")
t.start()


listener = keyboard.Listener(on_press=listen)
listener.start()


t.join()
print("finished")

exit()


import eventloop

eventloop.wrap(loop)

exit()


import cv2

worldmap = cv2.imread("resources/tmp/Capture.png", cv2.IMREAD_COLOR)
towerpart = cv2.imread("resources/tmp/lowerpart.PNG", cv2.IMREAD_COLOR)

_towers_ = util.find(towerpart, worldmap, threshold=0.7)
towers = typing.cast(list[Point],_towers_)

print(len(towers))
util.showMatches(towers, gui.dragon_cultist_free_npc_tower_level_3, worldmap)
exit()

pyautogui.sleep(2)
move_to()
