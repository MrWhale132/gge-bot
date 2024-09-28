import util
from common import AttackPanel, HorseSelectionMenu, Presets


def attack_with_preset(preset:int | None = None, first_wave_only=False, use_horses=False):
    if preset  is not None:
        util.click(AttackPanel.attack_preset_button_point)
        util.click(AttackPanel.nth_preset_button_point(preset))

    if first_wave_only:
        util.click(AttackPanel.apply_selected_preset_to_first_wave_button_point)
    else:
        util.click(AttackPanel.apply_selected_preset_to_all_wave_button_point)

    util.click(AttackPanel.launch_attack_button_point)
    if use_horses:
        util.click(HorseSelectionMenu.level_1_speed_boost_point)
    util.click(HorseSelectionMenu.confirm_button_point)
