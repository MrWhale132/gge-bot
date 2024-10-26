from config import *
import util
from uielements.gameobject import GameObject
from justtyping.justtypes import ScreenSection

import resources.symbol as gui
from resources.category import Image_rs


class Validator():...




class BasicImageValidator(Validator):

    def __init__(self,config:SimpleImageValidatorConfig, section:ScreenSection, image:Image_rs):
        if config is not None:
            self.section=config.section
            self.image=config.image
        else:
            self.section = section
            self.image = image


    def can_be_seen(self, gameobject:GameObject):
        assumed_location=util.screenshot(gameobject.section)
        sim = util.similar(gameobject.image,assumed_location)
        return sim

