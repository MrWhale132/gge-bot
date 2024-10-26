import time
import typing
import numpy as np

from config import TesseractConfig
from resources import symbol as gui

import util
from util import Point
from common import AttackPanel, ActionPalette, AttackConfirmationPanel, HorseSelectionMenu, Presets, OnCooldownPanel


def attack_with_preset(preset: int | None = None,
                       first_wave_only=False,
                       use_horses=False,
                       target: Point = None,
                       commander_whitelist:list[int]=None,commander_blacklist:list[int]=None,
                       fill_in_waves=False,
                       ):
    if target is not None:

        util.click(target)
        util.click(ActionPalette.attack_button_offset)
        util.click(AttackConfirmationPanel.confirm_button_point)
        time.sleep(1)

    if commander_whitelist is not None or commander_blacklist is not None:
        util.click(AttackPanel.next_available_commander(whitelist=commander_whitelist,blacklist=commander_blacklist),
                   waitAfterClick=0)

    if preset is not None:
        util.click(AttackPanel.attack_preset_button_point)
        util.click(AttackPanel.nth_preset_button_point(preset))

    if first_wave_only:
        util.click(AttackPanel.apply_selected_preset_to_first_wave_button_point)
    else:
        #todo deselcet all waves than select all except for courtyard
        util.click(AttackPanel.apply_selected_preset_to_all_wave_button_point)

    if fill_in_waves:
        util.click(AttackPanel.fill_in_waves_button_point)

    util.click(AttackPanel.launch_attack_button_point)
    # TODO do the same with the horses like with the nth_preset_button_point
    # as is this, it is unsuitable to choose from horses
    if use_horses:
        util.click(HorseSelectionMenu.level_1_speed_boost_point)
    util.click(HorseSelectionMenu.confirm_button_point)


def read_nth_commander_number(nth: int) -> int:
    digit_widths = [23, 40]  # single, double, triple...

    valid = False
    i = len(digit_widths) - 1

    while not valid and i > -1:
        width = digit_widths[i]
        number_section = (462, 620 + nth * 105, width, 35)  # double digit
        section = util.getSection(number_section)
        image = util.screenshot(section, gray=True)
        from config import TesseractConfig
        text = util.read(image, config=TesseractConfig.number_optimized().With(":"))
        util.showImg(image)  # debug
        print("read text: \"" + text + "\"")  # debug
        try:
            number = int(text)
            valid = True
        except:
            pass
        i -= 1
    else:
        if not valid:
            # TODO log
            print("Could not read commander number, therefore terminating the flow")
            exit()

    return number



def is_on_cooldown():
    """
        If the cooldown panel appears after selecting attack then this camp is occupied
        """
    # todo hardcoded
    time_skip_section = (1445, 625, 200, 80)
    section = util.getSection(time_skip_section)

    possible_timeskip_buttons_img = util.screenshot(section)
    # util.write_img(possible_timeskip_buttons_img,gui.open_timeskips_menu_buttons)
    # exit()
    # util.showImg(possible_timeskip_buttons_img)
    # util.showImg(util.loadImg(gui.open_timeskips_menu_buttons))

    _similar_, similarity = util.similar(possible_timeskip_buttons_img,
                                         gui.open_timeskips_menu_buttons,
                                         similarity_threshold=0.8, returnSimilarity=True)
    similar = typing.cast(bool, _similar_)
    print("occupied: ", similar, similarity)
    # exit()

    return similar



def skip_cooldown():
    util.click(OnCooldownPanel.open_timeskips_button_point)
    readCooldown()
    get_valid_cd()
    calc_minutes()
    create_timeskip_steps()
    move_into_scroll_area()
    execute_steps()



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

    util.scroll(steps[0].scrolls)

    currPos=0

    for i in range(1,len(steps)):
        currStep = steps[i]

        distance =currStep.scrolls-currPos
        util.scroll(distance)
        currPos = currStep.scrolls

        for i in range(currStep.clicks):
            util.click()
            print("click")