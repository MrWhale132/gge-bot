import time

import numpy
import pyautogui
from config import TesseractConfig

import util
from util import PointLike
from resources import ids as gui
from resources.ids import resource


def findCamps(campType: resource):
    global camps
    camps = util.find(campType,threshold=0.82)


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


def readTimeOnSkip():
    remaining_time_section = (
        1310, 550,
        100, 25
    )

    section = util.getSection(remaining_time_section)
    remaining_time_img = util.screenshot(section, gray=True)
    # util.showImg(remaining_time_img)
    # exit()

    config = TesseractConfig.number_optimized().With(time_comp_seperator)

    global remaining_time_text

    remaining_time_text = util.read(remaining_time_img, config=config)


    print(remaining_time_text)



    # TODO 30m and 1h is enough now but we should prepare it to use smaller time skips as well

    #TODO this type of cooldown validation needs to be outsourced



def get_valid_cd():
    global remaining_time_text


    def valid_format(text:str):
        if len(text) != 8: return False
        if text.count(time_comp_seperator) != 2: return False
        if not all([len(x) == 2 for x in text.split(time_comp_seperator)]): return False
        if not all([(x.isdigit() or x == ":") for x in text]): return False

        return True



    max_tries=3
    remaining_tries=max_tries

    while not valid_format(remaining_time_text) and remaining_tries > 0:
        remaining_tries -= 1
        print("The time format is invalid: " + remaining_time_text+". "+str(remaining_tries)+" attempts left")
        time.sleep(1.1) #100% sure that a whole second will pass
        readTimeOnSkip()
        # TODO handle exception
    else:
        if remaining_tries ==0:
            print("couldn't read time, going to assume its 50 min")
            #TODO this needs its own retry mechanicsm, for now we can assume
            #that if we cant scan the time than its cause the cooldown is at somewhere between 1h and 40 min
            remaining_time_text="00:55:00"
        else:
            print("time is valid")



def calc_minutes():

    time_comps_str: list[str] = remaining_time_text.split(time_comp_seperator)

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
    readTimeOnSkip()
    get_valid_cd()
    calc_minutes()
    create_timeskip_steps()
    move_into_scroll_area()
    execute_steps()


from util import Point
from common import ActionPalette, AtackConfirmationPanel


def start_attack(camp:Point):
    offset=Point(15,15,relative=True)
    middle = camp+offset

    util.click(middle)
    util.click(ActionPalette.attack_button_offset)



from common import OnCooldownPanel, AtackConfirmationPanel,Presets
from actions import attack_with_preset



def main():
    global camps

    from typing import NamedTuple

    class Camp(NamedTuple):
        location: Point
        isFree: bool


    findCamps(gui.occupied_nomad_camp)
    occupied_camps:list[Camp]=[Camp(camp,False) for camp in camps]
    # util.showMatches(camps,gui.occupied_nomad_camp)
    # print(len(occupied_camps))
    # exit()

    findCamps(gui.free_nomad_camp)
    free_camps:list[Camp]=[Camp(camp,True) for camp in camps]
    # util.showMatches(camps,gui.free_nomad_camp)
    # print(len(free_camps))
    # exit()

    allCamp:list[Camp] = occupied_camps+free_camps

    #TODO sometimes it happens that one camp gets found as free and occupied as well
    #different level of thresholds could be used but it may would be safer to just filter the duplicates
    print("#camps",len(allCamp))
    for camp in allCamp:
        print(camp.location)
    # exit()
    time.sleep(1)

    def run_flow(camp:Camp,preset:int=None):
        start_attack(camp.location)
        if not camp.isFree:
            skip_cooldown()
        util.click(AtackConfirmationPanel.confirm_button_point)
        time.sleep(2)
        attack_with_preset(preset)
    

    run_flow(allCamp[0],Presets.nomad)

    for i in range(1, len(allCamp)):
        camp = allCamp[i]
        run_flow(camp)

    exit()


import eventloop
eventloop.wrap(main)
exit()
