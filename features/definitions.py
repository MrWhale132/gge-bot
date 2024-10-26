from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from uielements.gameobject import GameObject

from justtyping.justtypes import ScreenSection
from resources.category import Image_rs

class Feature:
    def __init__(self, gameobject:GameObject):
        self.gameobject = gameobject


class IClickFeature(Feature):
    def click(self)->None:raise NotImplementedError



class IValidatorFeature(Feature):
    def validate(self, image:Image_rs, section:ScreenSection) ->bool: raise NotImplementedError

    def validate_go(self, gameobject: GameObject)->bool: raise NotImplementedError


