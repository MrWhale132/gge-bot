from __future__ import annotations

import time
from typing import Callable,override
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from uielements.gameobject import GameObject


from justtyping.justtypes import Point, ScreenSection

import features.definitions as definitions

from models.common import ClickStep


from resources.category import Image_rs

import util
from utils import mouse




class ClickFeature(definitions.IClickFeature):
    def __init__(self, gameobject:GameObject):
        super().__init__(gameobject)
        self.steps:list[ClickStep]=None

    def click(self):
        self.right_before_click()
        return
        for step in self.steps:
            step.play()



    def right_before_click(self):
        print("before")
        gameobject = self.gameobject
        ready_to_validate_pos = gameobject.click_point() + gameobject.before_validation_offset()
        mouse.move_mouse_curve(end=ready_to_validate_pos)

        validator = self.gameobject.getfeature(definitions.IValidatorFeature)
        if validator is not None:
            valid = validator.validate(self.gameobject.image, self.gameobject.section)

            if not valid:
                cleaner=self.gameobject.getfeature(PopUpCleaner)

                if cleaner is not None:
                    cleaner.clean()
                    mouse.click(self.gameobject)
            else:
                self.on_mouse_in_position()

    def on_mouse_in_position(self):
        print("on_mouse_in_position")
        mouse.move_mouse_straight(self.gameobject.position, duration=0.3)
        print("click")
        # mouse.click()



    @classmethod
    def default_two_stepped_click(cls, gameobject:GameObject)->ClickFeature:
        point_to_click = gameobject.click_point()
        offset= gameobject.before_validation_offset()

        # todo with this approach we can not parameterize the mouse's movement methods
        f = ClickFeature(gameobject)
        f.steps=[
                ClickStep(movement=lambda: mouse.move_mouse_curve(end=point_to_click + offset),
                          onStepComplete=f.right_before_click),

                ClickStep(movement=lambda: mouse.move_mouse_straight(end=point_to_click, duration=0.5),#hardcoded
                          onStepComplete=f.on_mouse_in_position)
            ]

        return f










class ImageValidator(definitions.IValidatorFeature):

    @override
    def validate(self, image:Image_rs, section:ScreenSection) ->bool:
        actual = util.screenshot(section)
        sim = util.similar(image, actual)
        return sim

    @override
    def validate_go(self,gameobject:GameObject)->bool:
        return self.validate(gameobject.image, gameobject.section)




class PopUpCleaner(definitions.Feature):
    def clean(self):
        from bot import state

        for popup in state.popups:
            print("focus",popup.infocus)
            if popup.isactive() and not popup.infocus or True:
                popup.handle()