package_abs_path_legth=len(__file__)-len("__init__.py")

def getRelPath(path):
    return path[package_abs_path_legth:-(len("/bind.py"))]

#TODO import all the classes from the subdirectories
from .units.unit_overview.barrack import _bind
from .buttons import _bind
from .storm import _bind
