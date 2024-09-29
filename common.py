from models.objects.Point import Point
import util
from typing import Callable


class ActionPalette:
    attack_button_offset: Point

    def __new__(cls, attack_button_offset):
        cls.attack_button_offset = attack_button_offset


ActionPalette(
    attack_button_offset=Point(130, 40,relative=True)
)


class AttackConfirmationPanel:
    confirm_button_point: Point

    def __new__(cls, confirm_button_point):
        cls.confirm_button_point = confirm_button_point


AttackConfirmationPanel(
    confirm_button_point=Point(1429, 932)
)



class AttackPanel:
    number_of_commanders_in_dropdown:int
    fill_in_waves_button_point:Point
    attack_preset_button_point: Point
    apply_selected_preset_to_first_wave_button_point: Point
    apply_selected_preset_to_all_wave_button_point: Point
    launch_attack_button_point: Point
    attack_presets_dropdown_section: dict

    def __new__(cls,
                attack_preset_button_point,
                attack_presets_dropdown_section,
                launch_attack_button_point,
                apply_selected_preset_to_first_wave_button_point,
                apply_selected_preset_to_all_wave_button_point,
                number_of_commanders_in_dropdown,
                fill_in_waves_button_point
                ):
        cls.attack_preset_button_point = attack_preset_button_point
        cls.attack_presets_dropdown_section = attack_presets_dropdown_section
        cls.launch_attack_button_point = launch_attack_button_point
        cls.apply_selected_preset_to_first_wave_button_point = apply_selected_preset_to_first_wave_button_point
        cls.apply_selected_preset_to_all_wave_button_point = apply_selected_preset_to_all_wave_button_point
        cls.number_of_commanders_in_dropdown = number_of_commanders_in_dropdown
        cls.fill_in_waves_button_point = fill_in_waves_button_point



    @staticmethod
    def nth_preset_button_point(nth:int)->Point:
        #todo hardcoded
        return Point(2000,1020 - nth*45)



    @staticmethod
    def nth_commander_point(nth:int)->Point:
        #todo hardcoded
        return Point(462, 620 + nth * 105)


    @staticmethod
    def read_commander_number_at(nth: int) -> int:
        digit_widths = [23, 40-3]  # single, double, triple...

        valid = False
        i = len(digit_widths) - 1

        while not valid and i > -1:
            width = digit_widths[i]
            nth_point=AttackPanel.nth_commander_point(nth)

            number_section = (462, 620 + nth * 105, width, 35)  # double digit

            # this 35+20 is extremely sensitive, even if you change it only by one pixel
            # tesseract won't be able to recognize it
            number_section=(
                nth_point.x,nth_point.y,
                width,35+20
            )

            section = util.getSection(number_section)
            image = util.screenshot(section,gray=True)

            from config import TesseractConfig

            text = util.read(image, config=TesseractConfig.number_optimized().With(":"))
            # util.showImg(image)  # debug
            # print("read text: \"" + text + "\"")  # debug
            # if i ==0:
            #     exit()
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





    @staticmethod
    def next_available_commander(whitelist:list[int]=None, blacklist:list[int]=None)->Point | None:
        if blacklist is not None and whitelist is not None:
            raise ValueError("black and white lists cannot be used together")

        if whitelist is not None:
            avaible:Callable[[int],bool]= lambda x: x in whitelist
        elif blacklist is not None:
            avaible: Callable[[int], bool] = lambda x: x not in blacklist
        else:
            avaible=lambda x:True


        #hardcoded
        #open the commander dropdown list
        util.click((550, 550),waiteBeforeClick=0,waitAfterClick=0)
        #move the mouse into the dropdown list area
        util.move_mouse_to(Point(0,100,relative=True),duration=0.2)


        #todo this solution is based on the promiese that there will always be an avaible commander
        # to see if the have reached the end of the dropdown list, we can check for the
        # premium commander portrait or the scroller component of the scrollable list
        tries=0
        # IMPORTANT: this curr is not the abs position, it's the position in the current dropdown list
        curr=0
        while not avaible(AttackPanel.read_commander_number_at(curr)) and tries < 50:
            #the next one would point outside the dropdown list
            if curr +1 == AttackPanel.number_of_commanders_in_dropdown:
                util.scroll(-1)
            else:
                curr+=1

            tries+=1
        else:
            if tries == 50:
                print("Could not find an available commander, therefore terminating the flow")
                exit()

        return AttackPanel.nth_commander_point(curr)


class Presets:
    nomad=4
    dragon_cultist=3


AttackPanel(
    attack_preset_button_point=Point(1950, 1050),
    launch_attack_button_point=Point(2000, 1300),
    fill_in_waves_button_point=Point(1900,970),
    apply_selected_preset_to_first_wave_button_point=Point(1825, 1125),
    apply_selected_preset_to_all_wave_button_point=Point(1955, 1125),
    attack_presets_dropdown_section=util.getSection((1800,410,500,700)),
    number_of_commanders_in_dropdown=7
)

#debug
#
# for i in range(7):
#     print(AttackPanel.read_commander_number_at(i))
#
# exit()





class HorseSelectionMenu:
    confirm_button_point:Point
    level_1_speed_boost_point:Point

    def __new__(cls, confirm_button_point, level_1_speed_boost_point):
        cls.confirm_button_point = confirm_button_point
        cls.level_1_speed_boost_point = level_1_speed_boost_point



HorseSelectionMenu(
    confirm_button_point=Point(1500, 1050),
    level_1_speed_boost_point=Point(1000, 700)
)







class OnCooldownPanel:
    open_timeskips_button_point:Point

    def __new__(cls, open_timeskips_button_point):
        cls.open_timeskips_button_point = open_timeskips_button_point



OnCooldownPanel(
    open_timeskips_button_point=Point(1600, 660)
)





