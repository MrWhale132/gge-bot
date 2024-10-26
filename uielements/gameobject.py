from __future__ import annotations



from resources import symbol as gui
from resources.category import Image_rs

from justtyping.justtypes import PointLike,Point
import justtyping.justtypes as jt


import util


class IInteractable:
    @property
    def is_clickable(self)->bool: raise NotImplementedError
    @property
    def can_beClicked(self)->bool: raise NotImplementedError
    @property
    def left_click_point(self) -> PointLike: raise NotImplementedError





from typing import TypeVar, Type, Dict, Optional, cast





class GameObject:
    def __init__(self,image:Image_rs, position:PointLike):
        if not isinstance(position, Point):
            position = Point(*position)


        self.position:Point = position

        self.image = image
        self.dimensions = image.image.shape[:2] #width, height


        self.features:Dict[Type[Feature], Feature]={}


        import features.feature as features
        from features.feature import ClickFeature,ImageValidator


        self.features[IClickFeature]=ClickFeature.default_two_stepped_click(self)
        self.features[IValidatorFeature]=ImageValidator(self)
        self.features[features.PopUpCleaner]=features.PopUpCleaner(self)


    def getfeature(self, feature:Type[TFeature])->Optional[TFeature]:
        _feature=self.features.get(feature)
        return cast(Optional[TFeature], _feature)


    def onclick(self):raise NotImplementedError


    def click_point(self)->PointLike:
        return self.position + (self.dimensions[1] // 2, self.dimensions[0] // 2)

    def before_validation_offset(self)->PointLike:
        #hardcoded
        return Point(100, 100, relative=True)


    @property
    def section(self)->jt.ScreenSection:
        params = [*self.position,*self.dimensions]
        _section= util.getSection(params)
        return _section



class Button(GameObject):...


class ActionPalette:
    class AttackButton(Button):
        def __init__(self, position: PointLike):
            super().__init__(gui.attack_option_button, position)







class NomadCamp(GameObject):
    def __init__(self, position: PointLike, image: Image_rs=None, occupied:bool=False):
        if image is None:
            if occupied:
                image = gui.occupied_nomad_camp
            else:
                image = gui.free_nomad_camp

        super().__init__(image, position)
        self.is_occupied = occupied







from features.definitions import Feature, IClickFeature, IValidatorFeature
TFeature=TypeVar("TFeature",bound=Feature)