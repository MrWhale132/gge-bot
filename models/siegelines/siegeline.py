from models.enums.flankside import FlankSide
from models.units.unit import Unit
from typing import List

from typing import Protocol

class IUnitContainer(Protocol):
    @property
    def Quantity(self) -> int:
        raise NotImplementedError


class UnitSlot:
    def __init__(self, unit: Unit, quantity: int):
        self._unit: Unit = unit
        self._quantity: int = quantity
        self._max: bool

    @property
    def Quantity(self)->int:
        return self._quantity

    @Quantity.setter
    def Quantity(self, value:int)->None:
        self._quantity+=value



slot = UnitSlot(None,10)
slot.Quantity=3
print(slot.Quantity)
exit()
class SiegeLine:
    def __init__(self):
        self._units: List[UnitSlot] = List[UnitSlot]()


class Front(SiegeLine):
    pass


class Flank(SiegeLine):

    def __init__(self, side: FlankSide):
        self._side = side


class CourtYard(SiegeLine):
    pass


class Wave:

    def __init__(self, **kwargs):
        self._front: Front = Front()
        self._leftFlank: Flank = Flank(FlankSide.left())
        self._rightFlank: Flank = Flank(FlankSide.right())

        self.__dict__.update(**kwargs)


class Attack:

    def __init__(self):
        self._waves: List[Wave] = List[Wave]()
        self._courtYard: CourtYard = CourtYard()
