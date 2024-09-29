import typing
from typing import Any, overload

import pytesseract, cv2, mss, pyautogui
import numpy as np
from cv2.typing import MatLike

from config import Config

from resources.ids import String_rs, image_rs, resource

CoordPairList = list[tuple[int, int]]
CoordLists = tuple[list[int], list[int]]

from typing import TypeGuard









def scroll(tick:int) -> None:
    print(f"scrolling: {tick}")
    if tick == 0: return

    direction = 1 if tick > 0 else -1
    for i in range(tick * direction): # dir * amount = always positive
        pyautogui.scroll(direction * 10)
        pyautogui.sleep(0.01)





def isCoordPairList(obj: Any) -> TypeGuard[CoordPairList]:
    # TODO type check of each element
    return (
            hasattr(obj, "__len__") and
            all(hasattr(x, "__len__") and len(x) == 2 for x in obj)
    )


def isCoordLists(obj: Any) -> TypeGuard[CoordLists]:
    return (
            hasattr(obj, "__len__") and
            len(obj) == 2 and
            hasattr(obj[0], "__len__") and
            hasattr(obj[1], "__len__") and
            len(obj[0]) == len(obj[1])
    )





def _uniqueCoordLists(locations: CoordLists) -> CoordLists:
    filtered: CoordLists = ([], [])
    if len(locations[0]) == 0: return filtered

    indices = list[int]()

    # xSorted=sorted(transpose(locations), key=lambda x: x[0])
    # print([coord[0] for coord in xSorted])
    # trans = transpose(xSorted)
    # print(trans[0])
    # exit()
    #an other array should be used
    locations =transpose( sorted(transpose(locations), key=lambda x: x[0]))[::-1]

    for i in range(0, len(locations[0])):
        y = locations[0][i]
        x = locations[1][i]
        prevY = locations[0][i - 1]
        prevX = locations[1][i - 1]

        distance = (x - prevX) ** 2 + (y - prevY) ** 2
        # print(distance)
        if distance > 1000:
            filtered[0].append(y)
            filtered[1].append(x)

    # if there was only one match than all the locations will be close to each other
    if len(locations) > 0 and len(filtered[0]) == 0:
        filtered[0].append(locations[0][0])
        filtered[1].append(locations[1][0])

    return filtered


def _uniqueCoordPairList(matches: CoordPairList) -> CoordPairList:
    return [(0, 1)]
    assert len(matches) > 0, "the nothing can't be made unique"

    filtered: CoordPairList = []

    if transposed:
        # list[(x,y)]
        length = len(matches)
        getDistance = lambda i: (matches[i][0] - matches[i - 1][0]) ** 2 + (matches[i][1] - matches[i - 1][1]) ** 2
    else:
        # list[list[y], list[x]]
        length = len(matches[0])
        getDistance = lambda i: (matches[0][i] - matches[0][i - 1]) ** 2 + (matches[1][i] - matches[1][i - 1]) ** 2

    for i in range(0, length):
        distance = getDistance(i)
        print(distance)
        if distance > 1000:
            filtered.append(matches[i])

    if len(filtered) == 0:
        filtered.append(matches[0])  # 0 length means there was only one match

    return filtered


def unique(locations: CoordPairList | CoordLists) -> CoordPairList | CoordLists:
    if isCoordPairList(locations):
        return _uniqueCoordPairList(locations)
    if isCoordLists(locations):
        # locations = typing.cast(CoordLists,locations)
        return _uniqueCoordLists(locations)

    raise ValueError(f"Invalid argument passed to unique: {locations}")


def showImg(img):
    cv2.imshow("Img", loadIfResource(img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()




from models.objects.Point import Point


def showMatches(matches:list[Point], of: resource | MatLike, in_: MatLike = None):
    if in_ is None:
        in_ = screenshot()

    of = loadIfResource(of)

    # Draw rectangles around the matches
    for loc in matches:
        cv2.rectangle(in_, loc.coordinates, (loc[0] + of.shape[1], loc[1] + of.shape[0]), (0, 255, 0), 2)

    # Create a named window and specify the window size
    window_name = 'Image Display'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Allow the window to be resizable
    cv2.resizeWindow(window_name, 1800, 1200)  # Set the window size (width, height)

    # Display the result (optional)
    cv2.imshow(window_name, in_)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


import root


def loadIfResource(resource_: resource):
    if isinstance(resource_, resource): return absLoad(resource_)
    return resource_


from plum import dispatch


@dispatch
def load(rs: resource):
    raise NotImplementedError(f"unknown resource type: {type(rs).__name__} ")


@dispatch
def load(text: String_rs) -> str:
    return open(absPath(text), mode="r", encoding="utf-8").read()


@dispatch
def load(image: image_rs) -> MatLike:
    return cv2.imread(absPath(image), cv2.IMREAD_COLOR)


def absPath(resource_: resource):
    return (f"{root.project_path}/{Config.resources_rel_path}/{resource_.path}/{resource_._name}")


def absLoad(resource_: resource):
    absPath = f"{root.project_path}/{Config.resources_rel_path}/{resource_.path}/{resource_._name}"
    return cv2.imread(absPath, cv2.IMREAD_COLOR)


def screenshot(section=None, to_cv2=True, gray=False):
    with mss.mss() as sct:
        if section is None: section = sct.monitors[1]
        screenshot = sct.grab(section)
    if to_cv2:
        return cv2.cvtColor(
            np.array(screenshot),
            cv2.COLOR_BGRA2GRAY if gray else cv2.COLOR_BGRA2RGB)
    else:
        return screenshot



#TODO move it to top
from config import TesseractConfig


def read(image: MatLike, numbers=False, config:TesseractConfig = TesseractConfig.default()) -> str:
    #TODO assert use numbers or config, but not both
    if numbers:
        _config:str = TesseractConfig.number_optimized().build()
    else:
        _config = config.build()

    return pytesseract.image_to_string(image, lang="hun", config=_config).strip()



from models.objects.Point import Point

def mousePos()->Point:
    pos = pyautogui.position()
    return Point(pos.x, pos.y)


def move_mouse_curve(start=None, end=None, func=lambda x: x ** 3, duration:float=1, steps=10):
    """
    Moves the mouse from `start` to `end` along a curve defined by `func`.

    Parameters:
    - start: Tuple[int, int] - Starting point (x, y).
    - end: Tuple[int, int] - Ending point (x, y).
    - func: Callable[[float], float] - A function defining the curvature.
           The function should take an x value (normalized between 0 and 1)
           and return a y value.
    - duration: float - Duration in seconds over which to complete the movement.
    - steps: int - Number of steps (points) to generate along the curve.
    """

    if start is None:
        start = mousePos()

    # Generate x values from 0 to 1
    x_values = np.linspace(0, 1, steps)
    y_values = [func(x) for x in x_values]

    # Calculate deltas for x and y
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    # Generate points along the curve
    points = [(start[0] + dx * x, start[1] + dy * y) for x, y in zip(x_values, y_values)]

    # Time to sleep between moves
    sleep_time = duration / steps

    # Move the mouse along the curve
    for point in points:
        pyautogui.moveTo(point[0], point[1], duration=sleep_time, tween=pyautogui.easeInOutQuad)
        # time.sleep(sleep_time)

from models.objects.Point import Point

PointLike = typing.Union[
    tuple[int, int],
    list[int, int],
    Point
]


def move_mouse_to(point: PointLike,duration:float=0.5):
    start = mousePos()

    if isinstance(point,Point) and point.relative:
        point = start + point

    move_mouse_curve(
        start=start,
        end=point,
        func=lambda x: x ** 3,
        duration=duration,
        steps=10
    )



def move_mouse_rel(point: PointLike):
    pos = mousePos()
    move_mouse_curve(
        start=pos,
        end=pos+point,
        func=lambda x: x ** 3,
        duration=1,
        steps=10
    )





def getSection(top, left, width, height):
    return {
        "top": top,
        "left": left,
        "width": width,
        "height": height
    }


def getSection(section)->dict:
    return {
        "top": section[1],
        "left": section[0],
        "width": section[2],
        "height": section[3]
    }




def find(image: resource | MatLike,
         in_: list | MatLike = None,
         transpose_=False,
         threshold=0.8,
         unique_=True,
         returnScreenshot=False,
         asPoints=True
         ) -> CoordLists | CoordPairList | list[Point]:

    assert transpose_ != asPoints

    if in_ is not None and returnScreenshot:
        raise ValueError("Currently there is no such situation where the user provided screenshot needs to be returned")

    if in_ is None or type(in_) is list:
        in_ = screenshot(section=in_)

    image = loadIfResource(image)

    # Convert the template image to RGB
    template_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use template matching to find the template in the screenshot
    result = cv2.matchTemplate(in_, template_rgb, cv2.TM_CCOEFF_NORMED)

    # Find where the matches occur
    locations: CoordLists = np.where(result >= threshold)
    # print(locations)
    if unique_:
        locations = _uniqueCoordLists(locations)

    if transpose_:
        locations: CoordPairList = transpose(locations)

    elif asPoints:
        locations:list[Point] = [Point(x,y) for x, y in zip(*locations[::-1])]

    if returnScreenshot:
        return locations, in_

    return locations



def transpose(locations):
    return list(zip(*locations[::-1]))


@overload
def click(waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:...

@overload
def click(point:Point,waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:...


from typing import Optional

def click(
        point:Optional[Point | tuple[int,int] | list[int, int]] = None,
        waiteBeforeClick:float =0.2,
        waitAfterClick:float = 0.1)\
        ->None:

    if point is not None:
        if not isinstance(point, Point):
            if isinstance(point,list | tuple):
                _point = Point(*point)
            else:
                raise TypeError("point must be Point or tuple/list of int")
        else:
            _point = point
        _move_to_than_click(_point, waiteBeforeClick, waitAfterClick)
    else:
        _just_click(waiteBeforeClick, waitAfterClick)


def _just_click(waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:
    if waiteBeforeClick > 0:
        pyautogui.sleep(waiteBeforeClick)

    pyautogui.click()

    if waitAfterClick > 0:
        pyautogui.sleep(waitAfterClick)


def _move_to_than_click(point: Point, waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:
    move_mouse_to(point)
    _just_click(waiteBeforeClick, waitAfterClick)





