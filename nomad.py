import time
import typing

import numpy as np
import pyautogui

import util
from config import TesseractConfig
from resources import symbol as gui
from resources.category import Resource
from justtyping.justtypes import PointLike

from uielements.gameobject import NomadCamp


#
# locations:list[PointLike]
# locations, screenshot = util.find(gui.dragon_cultist_free_npc_tower_level_3, threshold=0.8, returnScreenshot=True)
# print("#", len(locations))
# camps = [NomadCamp(gui.dragon_cultist_free_npc_tower_level_3,position=loc, occupied=False) for loc in locations]
# util.click(camps[0])
#
# exit()

#
#
# reward_popup=(1100, 700, 100, 100)
#
# section=util.getSection(reward_popup)
#
# img= util.screenshot(section, to_cv2=True)
# img= util.screenshot(section, to_cv2=False)
# # util.showImg(img)
# util.write_img(img,gui.nomad_individual_reward_popup)
# exit()
#




# #
# camps:list[Point]
# camps, screenshot = util.find(gui.occupied_nomad_camp,threshold=0.8,returnScreenshot=True)
# print("#",len(camps))
# for camp in camps:
#     print(camp)
# util.showMatches(camps,gui.occupied_nomad_camp,screenshot)
# exit()

def findCamps(campType: Resource = None)->None:
    global locations
    if campType is not None:
        locations = util.find(campType, threshold=0.9)
        return

    free=util.find(gui.free_nomad_camp,threshold=0.9)
    notfree=util.find(gui.occupied_nomad_camp,threshold=0.8)
    locations = free + notfree

    return


    #todo mock, hardcoded
    locations= [
        Point(1148, 437),
        Point(1226, 358),
        Point(1222, 1124),
        Point(1450, 1123),
    ]


def readTimeBeforeSkip():
    remaining_time_section = (
        1140, 670,
        150, 30
    )

    section = util.getSection(remaining_time_section)
    remaining_time_img = util.screenshot(section, gray=True)

    # util.showImg(remaining_time_img)

    remaining_time_text = util.read(remaining_time_img)
    # print(remaining_time_text)





time_comp_seperator = ":"


def readCooldown():
    # np.set_printoptions(threshold=np.inf)

    remaining_time_section = (
        1310, 550,
        100, 25
    )

    section = util.getSection(remaining_time_section)
    remaining_time_img = util.screenshot(section)


    black=0
    bg_color = remaining_time_img[10,10]
    #delete : between hour:min:sec, leaving only numbers
    remaining_time_img=np.delete(remaining_time_img,slice(61,66),axis=1)
    remaining_time_img=np.delete(remaining_time_img,slice(35,40),axis=1)
    # util.showImg(remaining_time_img)
    # exit()
    # remaining_time_img= np.insert(remaining_time_img,[65]*20+[40]*20, bg_color,axis=1)

    #todo hardcoded
    font_color = [74,59,40]
    remaining_time_img = util.thres(remaining_time_img,against=font_color,similarity=0.97)

    # util.showImg(remaining_time_img)
    # exit()

    config=TesseractConfig.number_optimized()


    global remaining_time_text

    start = time.time()
    remaining_time_text = util.read(remaining_time_img, config=config)
    end = time.time()
    print(remaining_time_text)
    # exit()



    # TODO 30m and 1h is enough now but we should prepare it to use smaller time skips as well




def get_valid_cd():
    global remaining_time_text


    #TODO this type of cooldown validation needs to be outsourced
    def valid_format(text:str):
        if len(text) != 6: return False
        if not all([(x.isdigit()) for x in text]): return False

        return True


    #todo hardcoded
    max_tries=5
    remaining_tries=max_tries

    while not valid_format(remaining_time_text) and remaining_tries > 0:
        remaining_tries -= 1
        print("The time format is invalid: " + remaining_time_text+". "+str(remaining_tries)+" attempts left")
        time.sleep(1.1) #100% sure that a whole second will pass
        readCooldown()
        # TODO handle exception
    else:
        if remaining_tries ==0:
            print("couldn't read a proper time, therefore exiting")
            exit()
        else:
            print("time is valid")



def calc_minutes():

    time_comps_str: list[str] = [remaining_time_text[2*i:2*i+2] for i in range(3)]

    try:
        time_comps = [int(x) for i, x in enumerate(time_comps_str)]
        seconds = [x * 60 ** (len(time_comps) - 1 - i) for i, x in enumerate(time_comps)]
        total_seconds: int = sum(seconds)

    except ValueError:
        print("Failed to parse time: " + remaining_time_text)
        # TODO handle exception
        exit()

    if total_seconds > 60 * 90:
        print("The cooldown of the camp is invalid: " + str(total_seconds / 60) + " (m)")


    global  minutes

    minutes = total_seconds /60
    print(minutes,"min" )




def create_timeskip_steps():
    global minutes

    from collections import namedtuple

    Step = namedtuple("Step", ["scrolls","clicks"])

    global steps

    steps = list[Step]()


    half_hours = minutes // 30
    print(half_hours)


    # TODO this whole scrolling feature should be made into an api
    # scroll to the 30 min and 1 hour time skip
    scroll_to_beginning = 5  # 1 min
    scroll_to_30m = -3
    scroll_to_1h = -4

    steps.append(Step(scroll_to_beginning, clicks=0))

    if half_hours == 2: #2x30 minutes + some leftover
        steps.extend([Step(scroll_to_30m,clicks=1),Step(scroll_to_1h,clicks=1)])
    elif half_hours == 1:
        steps.append(Step(scroll_to_30m, clicks=2))
    else:
        steps.append(Step(scroll_to_30m, clicks=1))



def move_into_scroll_area():
    use_time_skip_button_point = (1200, 750)


    util.move_mouse_to(use_time_skip_button_point)




def execute_steps():
    global steps

    scroll(steps[0].scrolls)

    currPos=0

    for i in range(1,len(steps)):
        currStep = steps[i]

        distance =currStep.scrolls-currPos
        scroll(distance)
        currPos = currStep.scrolls

        for i in range(currStep.clicks):
            util.click()
            print("click")




def scroll(tick:int) -> None:
    print(f"scrolling: {tick}")
    if tick == 0: return

    direction = 1 if tick > 0 else -1
    for i in range(tick * direction): # dir * amount = always positive
        pyautogui.scroll(direction * 10)
        pyautogui.sleep(0.01)




def skip_cooldown():
    util.click(OnCooldownPanel.open_timeskips_button_point)
    readCooldown()
    get_valid_cd()
    calc_minutes()
    create_timeskip_steps()
    move_into_scroll_area()
    execute_steps()


from util import Point
from common import ActionPalette, AttackConfirmationPanel


def isOccupied()->bool:
    """
    If the cooldown panel appears after selecting attack then this camp is occupied
    """
    #todo hardcoded
    time_skip_section = (1445, 625, 200, 80)
    section = util.getSection(time_skip_section)

    possible_timeskip_buttons_img = util.screenshot(section)
    # util.write_img(possible_timeskip_buttons_img,gui.open_timeskips_menu_buttons)
    # exit()
    # util.showImg(possible_timeskip_buttons_img)
    # util.showImg(util.loadImg(gui.open_timeskips_menu_buttons))

    _similar_,similarity = util.similar(possible_timeskip_buttons_img,
                                        gui.open_timeskips_menu_buttons,
                                        similarity_threshold=0.8, returnSimilarity=True)
    similar = typing.cast(bool,_similar_)
    print("occupied: ",similar, similarity)
    # exit()

    return  similar



def start_attack(camp:Point):
    offset=Point(15,10,relative=True)
    middle = camp+offset

    util.click(middle)
    util.click(ActionPalette.attack_button_offset,waitAfterClick=1)

    if isOccupied():
        skip_cooldown()

    util.click(AttackConfirmationPanel.confirm_button_point)
    time.sleep(1)



from common import OnCooldownPanel, AttackConfirmationPanel,Presets
from actions import attack_with_preset



def main():
    # isOccupied()
    # exit()
    findCamps()
    print("#", len(locations))
    def attack(camp, preset=None):
        start_attack(camp)

        attack_with_preset(preset, fill_in_waves=True,first_wave_only=True)

    attack(locations[0], Presets.nomad)
    for camp in locations[1:]:
        attack(camp)

if __name__ == "__main__":
    global remaining_time_text
    import eventloop
    eventloop.wrap(main).wait()
