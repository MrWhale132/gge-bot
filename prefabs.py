
from uielements.popups import SimplePopup

import justtyping.justtypes as jt
import resources.symbol as sym


class RubyOfferPopUp_1(SimplePopup):
    def __init__(self):
        #hardcoded
        close_button = Button(sym.ruby_offer_popup_1__close_button, (1515, 446))
        super().__init__(sym.ruby_offer_popup_1,(1075, 937), close_button)



class RubyOfferPopUp_2(SimplePopup):
    def __init__(self):
        #hardcoded
        close_button = Button(sym.ruby_offer_popup_1__close_button, (1686, 374))
        super().__init__(sym.ruby_offer_popup_2,(1090, 640), close_button)




class NomadPopUp(SimplePopup):
    def __init__(self):
        #hardcoded
        close_button = Button(image=sym.nomad_individual_reward_popup__accept_button,position=(1272, 879))
        super().__init__(sym.nomad_individual_reward_popup,(1064, 700), close_button)




from uielements.gameobject import GameObject, Button