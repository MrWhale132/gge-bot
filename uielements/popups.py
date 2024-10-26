from typing import override

from uielements.gameobject import GameObject,Button
import util
from utils import mouse

from resources.category import Image_rs
from justtyping.justtypes import PointLike


class Popup(GameObject):
    def __init__(self, image:Image_rs, pos:PointLike):
        super().__init__(image, pos)
        self._infocus = False

    def handle(self)->None: raise NotImplementedError
    def isactive(self)->bool: raise NotImplementedError
    @property
    def infocus(self)->bool: return self._infocus
    @infocus.setter
    def infocus(self, value: bool): self._infocus = value



class SimplePopup(Popup):
    def __init__(self, image_to_identify:Image_rs, pos_of_id_img:PointLike, close_button:Button):
        super().__init__(image_to_identify, pos_of_id_img)
        self.close_button = close_button


    @override
    def handle(self):
        print("handle")
        self.infocus=True
        mouse.click(self.close_button)
        self.infocus=False


    @override
    def isactive(self) -> bool:
        sim = util.similar(self.image,self.section)
        print("isactive: ",sim)
        return sim

