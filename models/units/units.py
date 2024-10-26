import util
from resources import symbol as gui
from models.units.unit import Unit, UnitMeta

UnitMeta.display_names.pop(None) #remove Unit's display_name


class VeteranDemonHorrorUnit(Unit):

    display_name = util.load(gui.veteran_demon_horror_unit__display_name)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

