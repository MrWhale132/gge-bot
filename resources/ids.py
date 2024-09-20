class resource:
    path:str
    def __init__(self, name):
        self._name = name
        # print(name)
        

class button_rs(resource): pass        
class image_rs(resource): pass

class realm_rs(resource): pass
class strom_rs(realm_rs): pass

class String_rs(resource): pass
class DisplayName_rs(String_rs): pass

class unit_rs(image_rs):
    def __init__(self, name, displayName):
        super().__init__(name)
        #TODO these infos also should be loaded from resources
        self._displayName = displayName
     
veteran_demon_horror_unit=unit_rs("veteran_demon_horror_unit.png",displayName="Veterán démonegység")
veteran_demon_horror_unit__display_name=DisplayName_rs("veteran_demon_horror_unit__display_name.txt")

fortress=strom_rs("fortress.png")

attack_option_button=button_rs("attack_option_button.png")
confirm_button=button_rs("confirm_button.png")
unit_slot=button_rs("unit_slot.png")
enter_castle_button=button_rs("enter_castle_button.png")
barrack_menu_button=button_rs("barrack_menu_button.png")
unit_overview_button=button_rs("unit_overview_button.png")
