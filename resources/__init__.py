from assertpy import assert_that

package_abs_path_legth=len(__file__)-len("__init__.py")

def getRelPath(path):
    filename = path.split("\\")[-1] #TODO / or \
    assert_that(filename).is_equal_to("_bind.py")
    
    return path[package_abs_path_legth:-(len("/_bind.py"))]

#TODO import all the classes from the subdirectories
from .units.unit_overview.barrack import _bind
from .buttons import _bind
from .storm import _bind
from .display_names import _bind
import resources.nomad._bind
import resources.firepeak._bind
