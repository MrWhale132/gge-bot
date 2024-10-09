from __future__ import annotations
from typing import Sequence

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from justtyping.justtypes import PointLike



class Point:

    def __init__(self, x=0, y=0, relative=False):
        self.x = x
        self.y = y
        self.relative = relative
        self.coordinates = [x, y]


    @staticmethod
    def From(
            x:int | PointLike | Sequence[PointLike],
            y:int=None)\
            ->Point | Sequence[Point]:

        if isinstance(x,int):
            assert y is not None,"can not use x without y"
            assert isinstance(y,int),"y must be an integer"

            return Point(x, y)

        assert y is None,"y can only be used if x is also a coordinate"

        if jtg.isPointLike(x):
            return Point(*x)

        if isinstance(x, Sequence):
            if len(x) == 0:
                return []

            if jtg.isPointLike(x[0]):
                return [Point(*i) for i in x]

        raise TypeError("Unsupported operand type(s) for Point.From: '{}'".format(type(x)))



    def __add__(self, other):
        if isinstance(other, tuple):
            if len(other) != len(self.coordinates):
                raise ValueError("Tuple dimensions must match Point dimensions")

            x, y = other[0],other[1]

        elif isinstance(other, Point):
            if not (not self.relative and other.relative):
                raise ValueError("Only a relative point can be added to an absolute point")

            x, y = other.x, other.y

        else:
            raise TypeError("Unsupported operand type(s) for +: 'Point' and '{}'".format(type(other)))

        return Point(self.x + x, self.y + y)


    def asCoordinates(self)->str:
        return f"({self.x}, {self.y})"

    def __getitem__(self, key):
        return self.coordinates[key]

    def __str__(self):
        return f"({self.x}, {self.y}, rel: {self.relative})"

    def __repr__(self):
        return self.__str__()


import justtyping.justtypeguards as jtg