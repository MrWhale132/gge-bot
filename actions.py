import time

import util
from util import Point
from common import AttackPanel, ActionPalette, AttackConfirmationPanel, HorseSelectionMenu, Presets


def attack_with_preset(preset: int | None = None, first_wave_only=False, use_horses=False, target: Point = None,
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


