from __future__ import annotations
from typing import TypeGuard, Any,Sequence

from typing import  TYPE_CHECKING
if TYPE_CHECKING:
    from justtyping.justtypes import Coordinate2D
    from justtyping.justtypes import PointLike



def isSequence(obj:Any):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__")


def isCoordinate2D(obj:Any)-> TypeGuard[Coordinate2D]:
    return (
        isSequence(obj) and
        len(obj) == 2 and
        hasattr(obj[0], 'is_integer') and hasattr(obj[1], 'is_integer')
    )

def isCoordinate2DSequence(obj:Any)-> TypeGuard[Sequence[Coordinate2D]]:
    return (
        isSequence(obj) and
        (len(obj) == 0 or isCoordinate2D(obj[0]))
    )

def isPointLike(obj:Any)-> TypeGuard[PointLike]:
    return (
        isinstance(obj,Point)
        or isCoordinate2D(obj)
    )

from models.objects.Point import Point
# PointLike ="XD"
