import pytesseract, cv2, mss, pyautogui
import numpy as np
from cv2.typing import MatLike

from config import Config
import gui_components as gui








def showMatches(matches, of: str | MatLike, in_:MatLike):
    
    of=loadIfString(of)
    
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



def loadIfString(img):
    if type(img) is str: return load(img)
    return img

def load(img:str):
    return cv2.imread(getimg(img), cv2.IMREAD_COLOR)

def getimg(filename:str):
    return Config.gui_comps_path+"/" + filename 
# Take a screenshot and convert it to a format OpenCV can work with


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
        
        
        
def read(image:MatLike) -> str:
    return pytesseract.image_to_string(image, lang="hun",config=Config.tesseract_config).strip()



def move_mouse_curve(start, end, func, duration=2, steps=100):
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



def find(image: str|MatLike, in_: list|MatLike =None, transpose_=True, threshold=0.8):
    
    if in_ is None or type(in_) is list:
        screen_rgb =screenshot(section=in_)

    image=loadIfString(image)

    # Convert the template image to RGB
    template_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use template matching to find the template in the screenshot
    result = cv2.matchTemplate(screen_rgb, template_rgb, cv2.TM_CCOEFF_NORMED)

    # Find where the matches occur
    locations = np.where(result >= threshold)
    
    if transpose_:
        locations = transpose(locations)
    
    return locations


def transpose(locations):
    return list(zip(*locations[::-1]))