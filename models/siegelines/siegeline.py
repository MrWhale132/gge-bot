# from models.enums.flankside import FlankSide
# from models.units.unit import Unit
# from typing import override, Union
#


from typing import Protocol

class Adder(Protocol):
    def add(self, x:int, y): ...

class IntAdder:
    def add(self, x:str, y):
        return x + y

class FloatAdder:
    def add(self, x, y):
        return x + y

def add(adder: Adder) -> None:
    print(adder.add(2, 3))


class NoAdd:
    def add(self,x,y):
        return x-4

taker = NoAdd()

add(taker)

add(IntAdder())
add(FloatAdder())



exit()


class IUnitContainer:
    @property
    def Quantity(self):
        raise NotImplementedError



class UnitSlot(IUnitContainer):
    test = Union[int | str]
    @override
    @property
    def Quantity(self):
        return  self._quantity

    def __init__(self, unit:Unit, quantity:int):
        self._unit:Unit=unit
        self._quantity:int=quantity
        self._max:bool

slot = UnitSlot(None,10)
print(slot.Quantity)
exit()

class SiegeLine:
    def __init__(self):
        self._units:List[Unit]=List[Unit]()

class Front(SiegeLine):
    pass

class Flank(SiegeLine):

    def __init__(self, side:FlankSide):
        self._side =side

class CourtYard(SiegeLine):
    pass

class Wave:

    def __init__(self, **kwargs):
        self._front:Front = Front()
        self._leftFlank:Flank = Flank()
        self._rightFlank:Flank = Flank()

        self.__dict__.update(**kwargs)

from typing import List, override


class Attack:

    def __init__(self):
        self._waves:List[Wave]= List[Wave]()
        self._courtYard:CourtYard = CourtYard()

