from posixpath import abspath
import pytesseract, cv2, mss, pyautogui
import numpy as np
from cv2.typing import MatLike

from config import Config

from resources.ids import String_rs, image_rs, resource




def showImg(img):
    cv2.imshow("Img", loadIfResource(img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def showMatches(matches, of: resource | MatLike, in_:MatLike):
    
    of=loadIfResource(of)
    
    # Draw rectangles around the matches
    for loc in matches:
        cv2.rectangle(in_, loc, (loc[0] + of.shape[1], loc[1] + of.shape[0]), (0, 255, 0), 2)

    # Create a named window and specify the window size
    window_name = 'Image Display'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Allow the window to be resizable
    cv2.resizeWindow(window_name, 1800, 1200)  # Set the window size (width, height)

    # Display the result (optional)
    cv2.imshow(window_name, in_)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



import root

def loadIfResource(resource_:resource):
    if isinstance(resource_,resource): return absLoad(resource_)
    return resource_




from plum import dispatch


@dispatch
def load(rs: resource):
    raise NotImplementedError(f"unknown resource type: {type(rs).__name__} ")
 
@dispatch
def load(text:String_rs) -> str:
    return open(absPath(text),mode="r",encoding="utf-8").read()
    

@dispatch
def load(image:image_rs) -> MatLike:
    return cv2.imread(absPath(image), cv2.IMREAD_COLOR)



def absPath(resource_: resource):
    return ( f"{root.project_path}/{Config.resources_rel_path}/{resource_.path}/{resource_._name}")

def absLoad(resource_: resource):
    absPath=f"{root.project_path}/{Config.resources_rel_path}/{resource_.path}/{resource_._name}"
    return cv2.imread(absPath, cv2.IMREAD_COLOR)




def screenshot(section = None, to_cv2=True, gray=False):
    with mss.mss() as sct:
        if section is None: section =sct.monitors[1]
        screenshot= sct.grab(section)
    if to_cv2:
        return cv2.cvtColor(
            np.array(screenshot),
            cv2.COLOR_BGRA2GRAY if gray else cv2.COLOR_BGRA2RGB)
    else:
        return screenshot
        
        
        
def read(image:MatLike, text=False) -> str:
    config = None if text else Config.tesseract_config
    return pytesseract.image_to_string(image, lang="hun",config=config).strip()



def mousePos():
    pos =pyautogui.position()
    return pos[0], pos[1]


    
def move_mouse_curve(start=None, end=None, func=lambda x: x**3, duration=1, steps=10):
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
        



def getSection(top, left, width, height):
    return {
        "top": top,
        "left": left,
        "width": width,
        "height": height
    }

def getSection(section):
    return {
        "top": section[1],
        "left": section[0],
        "width": section[2],
        "height": section[3]
    }



def find(image: resource|MatLike, in_: list|MatLike =None, transpose_=True, threshold=0.8):
    
    if in_ is None or type(in_) is list:
        in_ =screenshot(section=in_)

    image=loadIfResource(image)

    # Convert the template image to RGB
    template_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use template matching to find the template in the screenshot
    result = cv2.matchTemplate(in_, template_rgb, cv2.TM_CCOEFF_NORMED)

    # Find where the matches occur
    locations = np.where(result >= threshold)
    
    if transpose_:
        locations = transpose(locations)
    
    return locations


def transpose(locations):
    return list(zip(*locations[::-1]))