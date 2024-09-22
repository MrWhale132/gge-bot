from __future__ import annotations


class FlankSide:
    @classmethod
    def right(cls)-> FlankSide:
        return FlankSide("right")
    @classmethod
    def left(cls)->FlankSide:
        return FlankSide("left")

    def __init__(self, side:str):
        self._side =side

    def __eq__(self, other:object)->bool:
        if not isinstance(other, FlankSide):
            return False

        return self._side == other._side
