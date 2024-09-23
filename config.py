from __future__ import annotations
from typing import Optional, Any, List


class TesseractConfig:
    def __init__(self, whitelist:Optional[list[str]] = None, **kwargs:dict[str,Any]) -> None:
        self.whitelist = whitelist
        self._oem:int = 3
        self._psm: int = 7
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

    def With(self, whitelist_chars:str)->TesseractConfig:
        for char in whitelist_chars:
            self.add_whitelist_char(char)

        return self


    def build(self)->str:
        config =f'--oem {self._oem} --psm {self._psm}'
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
