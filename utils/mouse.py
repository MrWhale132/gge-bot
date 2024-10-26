from __future__ import annotations
from typing import overload, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from uielements.gameobject import GameObject
from justtyping.justtypes import PointLike

from models.objects.Point import Point

import pyautogui
import numpy as np


@overload
def click(waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:...

@overload
def click(point:PointLike,waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1)->None:...

@overload
def click(point:PointLike,waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1,moveDuration:float = 0.5)->None:...
@overload
def click(point:GameObject,waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1,moveDuration:float = 0.5)->None:...






def click(
        point:Optional[PointLike | GameObject] = None,
        waiteBeforeClick:float =0.2,
        waitAfterClick:float = 0.1,
        moveDuration:float = 0.5)\
        ->None:
    from uielements.gameobject import GameObject

    if isinstance(point,GameObject):
        feature = point.getfeature(IClickFeature)
        feature.click()
        return


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


def _move_to_then_click(point: PointLike, waiteBeforeClick:float =0.1, waitAfterClick:float = 0.1, duration:float = 0.5)->None:
    move_mouse_to(point,duration=duration)
    _just_click(waiteBeforeClick, waitAfterClick)



@overload
def double_click()->None:...

@overload
def double_click(point:PointLike)->None:...


def double_click(point:PointLike =None)->None:
    click(point,waitAfterClick=0)
    click(waiteBeforeClick=0.1,waitAfterClick=0)








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





from justtyping.justtypes import PointLike


def move_mouse_straight(end:PointLike,duration:float=1):
    pyautogui.moveTo(end[0], end[1], duration=duration, tween=pyautogui.easeInOutQuad)





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



from features.definitions import IClickFeature