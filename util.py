from __future__ import annotations
import builtins
import typing
from typing import Any, overload, Sequence, TYPE_CHECKING

import pytesseract, cv2, mss, pyautogui
import numpy as np
from cv2.typing import MatLike

from resources.category import String_rs, Image_rs, Resource


CoordPairList = list[tuple[int, int]]
CoordLists = tuple[list[int], list[int]]

from typing import TypeGuard
from typing import Union


import justtyping.justtypes as jt
from justtyping.justtypes import ScreenSection





#IMPORTANT
#todo we use a 0.8 threshold to account for flux's blue light filtering
def similar(imageA:np.ndarray | Resource, imageB:np.ndarray | Resource | ScreenSection, similarity_threshold:float = 0.95, returnSimilarity:bool = False)\
        -> bool | tuple[bool,float]:

    if isinstance(imageB,ScreenSection):
        imageB = screenshot(imageB)

    elif isinstance(imageB,Image_rs):
        imageB=loadImg(imageB)

    imageA = loadIfResource(imageA)

    assert imageA.shape == imageB.shape, f"the shape of the images must match, shape A: {imageA.shape}, shape B: {imageB.shape}"

    result = cv2.matchTemplate(imageA, imageB, cv2.TM_CCOEFF_NORMED)
    # print(result)
    assert len(result) == 1, "for the image with the same shape there should be only one match result"

    similarity =typing.cast(float,result[0,0])
    _similar = similarity >= similarity_threshold

    if returnSimilarity:
        return _similar, similarity

    return _similar


    # unfortunately this does not work as I imagined.
    # imageB=loadImg(imageB)
    # assert imageA.shape == imageB.shape, "the shape of the images must match"
    #
    # max_diff=255**2
    # for dim in imageA.shape:
    #     max_diff*=dim
    #
    # diff=np.sum((imageA-imageB)**2)
    # print("diff",diff, max_diff, diff/max_diff)
    # similarity= 1-diff/max_diff
    #
    # return similarity>=similarity_threshold, similarity



def thres(image:np.array, against:Union[list[int,int,int], np.array], similarity:float)->np.array:
    thresed=image.copy()

    max_distance=sum(np.array([255,255,255])**2)

    font_color = against
    if not isinstance(against, np.ndarray):
        font_color = np.array(against)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            pixel = image[y, x]
            squared_distance = sum((pixel-font_color)**2)
            _similarity = 1-squared_distance/max_distance

            if _similarity >= similarity:
                thresed[y, x] = [255, 255, 255]
            else:
                thresed[y, x] = [0, 0, 0]

    return thresed



def typeIn(keys: str | list, interval: float = 0.1):
    _keys = keys
    if isinstance(keys, str):
        _keys=list(keys)
    pyautogui.press(list(_keys),interval=interval)


from models.objects.Point import Point




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


from typing import Callable
from justtyping.justtypes import Coordinate2D
from justtyping.justtypeguards import isCoordinate2D


class Group():
    def __init__(self):
        self.elements: list[Coordinate2D] = []


    def add(self, element: Coordinate2D):
        self.elements.append(element)

    def isOccupied(self):
        return True


from typing import override



class ElementField(Group):
    def __init__(self, dimension:tuple[int,int]):
        width = dimension[0]
        height = dimension[1]
        self.width = width
        self.height = height

        self.fieldDimension = dimension
        self.field:list[list[Group]] =[[self]*width for _ in range(height)]

        self.groups:list[Group]=[]

        self.group_occupation_area_half_side_length = 15


    def group(self, elements:list[Coordinate2D]):
        for element in elements:
            self.addElement(element)

    def keys(self)->list[Coordinate2D]:
        return [group.elements[0] for group in self.groups]


    def addElement(self, element: Coordinate2D):
        self._get(element).add(element)


    @override
    def add(self, element: Coordinate2D):
        newGroup = Group()
        newGroup.add(element)

        group_occupation_area_half_side_length =15

        #square
        #upper left corner
        xStart = element[0] - self.group_occupation_area_half_side_length
        yStart = element[1] - self.group_occupation_area_half_side_length

        #lower right corner
        xEnd = element[0] + self.group_occupation_area_half_side_length + 1
        yEnd= element[1] + self.group_occupation_area_half_side_length + 1

        #todo optimize, instead of accessing one row multiple times, get the row once
        for y in range(yStart,yEnd):
            for x in range(xStart,xEnd):
                if 0 <= y < self.height and 0 <= x < self.width:
                    pos =(x,y)
                    if not self._get(pos).isOccupied():
                        self._set(pos, newGroup)

        self.groups.append(newGroup)


    @override
    def isOccupied(self):
        return False


    def _set(self, at:Coordinate2D, group:Group):
        self.field[at[1]][at[0]]=group


    def _get(self, at:Coordinate2D):
        return self.field[at[1]][at[0]]


    #debug
    def printField(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self._get((x,y)).isOccupied():
                    print("X", end="")
                else:
                    print(".", end="")
            print()



from justtyping.justtypes import PointLike


def _unique(locations:list[PointLike])-> list[PointLike]:
    if len(locations) ==0:
        return []

    height = max([loc[1] for loc in locations])+1
    width = max([loc[0] for loc in locations])+1

    field = ElementField((width, height))
    field.group(locations)

    return field.keys()



def _uniqueCoordLists(locations: CoordLists) -> CoordLists:
    filtered: CoordLists = ([], [])
    if len(locations[0]) == 0: return filtered

    height = max(locations[1])
    width = max(locations[0])

    field = ElementField((width,height))
    coordinates = np.transpose(locations[::-1])
    field.group(coordinates)

    return field.keys()

    # #an other array should be used
    # print(locations)
    # print(np.transpose(locations[::-1]))
    # exit()
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
    raise NotImplementedError("out of service")
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
    raise NotImplementedError("out of service")
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


def showMatches(matches:list[Point], of: Resource | MatLike = None, in_: MatLike = None):
    if in_ is None:
        in_ = screenshot()

    of = loadIfResource(of)

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


def loadIfResource(resource_: Resource):
    if isinstance(resource_, Resource): return absLoad(resource_)
    return resource_


from plum import dispatch


@dispatch
def load(rs: Resource):
    raise NotImplementedError(f"unknown resource type: {builtins.type(rs).__name__} ")


@dispatch
def load(text: String_rs) -> str:
    return open(absPath(text), mode="r", encoding="utf-8").read()





@dispatch
def load(image: Image_rs) -> MatLike:
    return cv2.imread(absPath(image), cv2.IMREAD_COLOR)




from assertpy import assert_that

def loadImg(image:Resource)-> np.ndarray:
    assert_that(image._name).ends_with(".png")

    from config import Config

    absPath = f"{root.project_path}/{Config.resources_rel_path}/{image.namespace}/{image._name}"
    return cv2.imread(absPath, cv2.IMREAD_COLOR)



def absPath(resource_: Resource):
    from config import Config

    return (f"{root.project_path}/{Config.resources_rel_path}/{resource_.namespace}/{resource_._name}")


def absLoad(resource_: Resource):
    from config import Config

    absPath = f"{root.project_path}/{Config.resources_rel_path}/{resource_.namespace}/{resource_._name}"
    return cv2.imread(absPath, cv2.IMREAD_COLOR)



from mss.screenshot import ScreenShot

def screenshot(section=None, to_cv2=True, gray=False)->np.ndarray | ScreenShot:

    with mss.mss() as sct:
        if section is None: section = sct.monitors[1]
        screenshot = sct.grab(section)

    img_np = np.array(screenshot)

    if gray:
        return cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY)

    if to_cv2:
        return  cv2.cvtColor(img_np,cv2.COLOR_RGBA2RGB)

    return screenshot




import mss.tools
#todo currently we can not say param:ImageResource
def write_img(image:ScreenShot, into:Resource):
    assert type(image) is ScreenShot, "image must be a ScreenShot, you probably forgot to NOT to turn the sceenshot into cv2 format"

    path = absPath(into)
    mss.tools.to_png(image.rgb, image.size, output=path)



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
from justtyping.justtypes import PointLike



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
        "width": section[3],
        "height": section[2]
    }




def getsection(topleft:PointLike, bottomrigth:PointLike):
    return {
        "top": topleft[1],
        "left": topleft[0],
        "width": bottomrigth[0] - topleft[0],
        "height": bottomrigth[1] - topleft[1]
    }


from justtyping.justtypes import PointLike


def find(image: Resource | MatLike,
         in_: list | MatLike = None,
         transpose_=True,
         threshold=0.7, # it is that low to account for flux's blue light filtering
         unique_=True,
         returnScreenshot=False,
         asPoints=True
         ) -> CoordLists | CoordPairList | list[Point]:

    # assert transpose_ != asPoints

    if in_ is not None and returnScreenshot:
        raise ValueError("Currently there is no such situation where the user provided screenshot needs to be returned")

    if in_ is None or builtins.type(in_) is list:
        in_ = screenshot(section=in_)

    image = loadIfResource(image)


    # Use template matching to find the template in the screenshot
    result = cv2.matchTemplate(in_, image, cv2.TM_CCOEFF_NORMED)

    # Find where the matches occur
    locations: CoordLists = np.where(result >= threshold)
    # print(result[locations])

    locations:list[PointLike] = np.transpose(locations[::-1]) #mypy ignore

    locations= typing.cast(list[PointLike], locations)

    # print(locations)
    if unique_:
        print("before ",len(locations))
        locations = _unique(locations)
        print("after ", len(locations))

    if not transpose_:
        locations: CoordLists = np.transpose(locations[::-1]) #mypy ignore

    elif asPoints:
        locations:Sequence[Point] = Point.From(locations)

    if returnScreenshot:
        return locations, in_

    return locations



def transpose(locations):
    return list(zip(*locations[::-1]))


@overload
def click(waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:...

@overload
def click(point:Point,waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:...

@overload
def click(point:Point,waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1,moveDuration:float = 0.5)->None:...


from typing import Optional

if TYPE_CHECKING:
    from uielements.gameobject import GameObject


def click(
        point:Optional[Point | tuple[int,int] | list[int, int] | GameObject] = None,
        waiteBeforeClick:float =0.2,
        waitAfterClick:float = 0.1,
        moveDuration:float = 0.5)\
        ->None:
    from uielements.gameobject import GameObject

    isinstance(point,GameObject)
    if point is not None:
        if not isinstance(point, Point):
            if isinstance(point,list | tuple):
                _point = Point(*point)
            else:
                raise TypeError("point must be Point or tuple/list of int")
        else:
            _point = point
        _move_to_then_click(_point, waiteBeforeClick, waitAfterClick, duration=moveDuration)
    else:
        _just_click(waiteBeforeClick, waitAfterClick)


def _just_click(waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:
    if waiteBeforeClick > 0:
        pyautogui.sleep(waiteBeforeClick)

    pyautogui.click()

    if waitAfterClick > 0:
        pyautogui.sleep(waitAfterClick)


def _move_to_then_click(point: Point, waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1, duration:float = 0.5)->None:
    move_mouse_to(point,duration=duration)
    _just_click(waiteBeforeClick, waitAfterClick)



@overload
def double_click()->None:...

@overload
def double_click(point:Point | tuple[int,int])->None:...


def double_click(point:Point | tuple[int,int])->None:
    click(point,waitAfterClick=0)
    click(waiteBeforeClick=0.1,waitAfterClick=0)




