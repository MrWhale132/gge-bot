import pyautogui

from actions import attack_with_preset
from common import Presets
from util import Point

from config import CommanderConfig

blacklist = CommanderConfig.barbarian_tower_blacklist_commanders


def attack(tower: Point, preset=None):
    attack_with_preset(target=tower, preset=preset, use_horses=True, commander_blacklist=blacklist, first_wave_only=True,fill_in_waves=True)



def inner_ring():
    #TODO comeback later when we have a more accurate image finder
    towers:list[Point]=[
        Point(1368,813),
        Point(1443,1354),
        Point(1060,970),
        Point(834,1200),
        Point(600,886),
        Point(520,580),
        Point(910,500),
        Point(990,120),
        Point(1370,200),
        Point(1450,510),
        Point(1835,360),
        Point(2135,435),
        Point(1985,740),
        Point(1905,1010), #they are outside the screen
        Point(990,1310),
    ]

    print("inner ring")

    attack(towers[0],Presets.dragon_cultist)

    for i in range(1,13):
        attack(towers[i])

    pyautogui.dragRel(0,-200,duration=1)

    for i in range(13,15):
        attack(towers[i])





def outer_ring():
    from common import WorldMapView

    WorldMapView.goto((769,514))

    first = Point(443, 278)
    attack(first,Presets.npc)

    towers =[
        Point(677, 498),
        Point(754, 203),
        Point(1064, 509),
        Point(1290, 202),
        Point(1601, 742),
        Point(1907, 901),
        Point(1596, 281),
        Point(1831, 514),
        Point(2140, 671)
    ]

    for t in towers:
        attack(t)


    WorldMapView.goto((775,527))


    towers = [
        Point(1826, 277),
        Point(1441, 439),
        Point(1672, 661),
        Point(1447, 896),
        Point(1601, 1204)
    ]

    for t in towers:
        attack(t)


if __name__ == '__main__':
    import eventloop
    eventloop.wrap(inner_ring).wait()
    print("main is exiting")

