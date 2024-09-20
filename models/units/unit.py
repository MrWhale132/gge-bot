
class UnitMeta(type):
    display_names={}

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        if "display_name" in dct: #TODO find a solution to avoid strings
            UnitMeta.display_names.update({dct["display_name"]: cls})

class Unit(metaclass=UnitMeta):

    display_name:str=None
    quantity=int

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
