from models.objects.Point import Point
import util


class ActionPalette:
    attack_button_offset: Point

    def __new__(cls, attack_button_offset):
        cls.attack_button_offset = attack_button_offset


ActionPalette(
    attack_button_offset=Point(130, 40,relative=True)
)


class AtackConfirmationPanel:
    confirm_button_point: Point

    def __new__(cls, confirm_button_point):
        cls.confirm_button_point = confirm_button_point


AtackConfirmationPanel(
    confirm_button_point=Point(1429, 932)
)



class AttackPanel:
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
                apply_selected_preset_to_all_wave_button_point
                ):
        cls.attack_preset_button_point = attack_preset_button_point
        cls.attack_presets_dropdown_section = attack_presets_dropdown_section
        cls.launch_attack_button_point = launch_attack_button_point
        cls.apply_selected_preset_to_first_wave_button_point = apply_selected_preset_to_first_wave_button_point
        cls.apply_selected_preset_to_all_wave_button_point = apply_selected_preset_to_all_wave_button_point



    def nth_preset_button_point(nth:int)->Point:
        return Point(2000,1020 - nth*45)



class Presets:
    nomad=4
    dragon_cultist=3


AttackPanel(
    attack_preset_button_point=Point(1950, 1050),
    launch_attack_button_point=Point(2000, 1300),
    apply_selected_preset_to_first_wave_button_point=Point(1825, 1125),
    apply_selected_preset_to_all_wave_button_point=Point(1955, 1125),
    attack_presets_dropdown_section=util.getSection((1800,410,500,700))
)




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