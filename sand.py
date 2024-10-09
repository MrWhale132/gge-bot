import time

import pyautogui

import util
from actions import attack_with_preset
from common import Presets
from models.objects.Point import Point




def main():
    #TODO comeback later when we have a more accurate image finder
    towers:list[Point]=[
        Point(1525, 930),
        Point(1214, 1158),
        Point(986, 707),
        Point(834, 1008),
        Point(601, 628),
        Point(832, 315),
        Point(1448, 389),
        Point(1757, 469),
        Point(2063, 933),
        Point(1832, 1161),
    ]

    from config import CommanderConfig
    blacklist = CommanderConfig.barbarian_tower_blacklist_commanders


    def attack(tower:Point, preset=None):
        attack_with_preset(target=tower,preset=preset,use_horses=True,commander_blacklist=blacklist)

    #
    #
    util.move_mouse_to((1094, 714))
    #
    pyautogui.dragRel(0,-200,duration=1)
    #
    # #
    attack(towers[0],Presets.npc)

    for i in range(1,10):
        attack(towers[i])


    #todo beacuse game lag, we cannot rely on that dragging will positioning the screen properly
    pyautogui.dragRel(0,800,duration=2.5)


    towers=[
        Point(912, 390),
        Point(1215, 238),
        Point(1524, 158),
        Point(1831, 466),
        Point(2216, 621)
    ]

    for i in range(0,5):
        attack(towers[i])


if __name__ == '__main__':
    import eventloop
    eventloop.wrap(main).wait()
    print("main is exiting")