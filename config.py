from __future__ import annotations
from typing import Optional, Any, List

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from justtyping.justtypes import ScreenSection
    from resources.symbol import Image_rs





class TesseractConfig:
    def __init__(self, whitelist:Optional[list[str]] = None, **kwargs:dict[str,Any]) -> None:
        self.whitelist = whitelist
        self._oem:int = 3
        self.psm_: int = 7
        self.__dict__.update(**kwargs)

    @staticmethod
    def default() -> TesseractConfig:
        return TesseractConfig(
            whitelist=[]
        )


    @staticmethod
    def number_optimized() -> TesseractConfig:
        return TesseractConfig(
            whitelist=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        )


    @staticmethod
    def nomad_cd()->TesseractConfig:
        config = TesseractConfig.number_optimized().With(":")
        config.psm_=7
        return config


    def With(self, whitelist_chars:str)->TesseractConfig:
        for char in whitelist_chars:
            self.add_whitelist_char(char)

        return self


    def build(self)->str:
        config =f'--oem {self._oem} --psm {self.psm_}'
        if len(self.whitelist) != 0:
            config += f' -c tessedit_char_whitelist={"".join(self.whitelist)}'

        return  config


    def add_whitelist_char(self,char:str):
        if len(char) != 1:
            raise ValueError("Character must be a single character.")

        self.whitelist.append(char)



class Config:
    resources_rel_path = "resources"
    # number specific
    tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'



class CommanderConfig:
    storm_relic_commander=13
    storm_non_relic_commanders=[*range(16,19)]
    storm_commanders=[storm_relic_commander]+storm_non_relic_commanders

    npc_event_commanders=[*range(1,6)]

    barbarian_tower_blacklist_commanders=storm_commanders






class SimpleImageValidatorConfig:
    def __init__(self, section:ScreenSection, image:Image_rs):
        self.section = section
        self.image = image



class SimpleImageValidatorConfigSource:
    util=None
    gui=None

    def __new__(cls, *args, **kwargs):
        import util
        cls.util = util
        from resources import symbol as gui
        cls.gui = gui


    @classmethod
    def samurai_reward(cls)-> SimpleImageValidatorConfig:
        return SimpleImageValidatorConfig(cls.util.getSection((1130,710, 30,60)),cls.gui.samurai_individual_reward_popup)

    @classmethod
    def ruby_offer_1(cls) -> SimpleImageValidatorConfig:
        return SimpleImageValidatorConfig(cls.util.getSection((1080,935,60,60)),cls.gui.ruby_offer_popup_1)

    # ruby_offer_2=SimpleImageValidatorConfig(util.getSection((1065,630,100,80)),gui.ruby_offer_popup_2)


