import cv2
import pyautogui

from util import *
from gui_components import *


while True:
    
    # unit qty check
    first_unit_qty_x=840
    first_unit_qty_y=343
    unit_qty_box_width=35
    unit_qty_box_height=17
    y_correction=0
    for i in range(0,4):
        unit_qty_section=(
            first_unit_qty_x,
            first_unit_qty_y +i*59-(i//3*2),
            unit_qty_box_width,
            unit_qty_box_height)
        
        unit_qty_section = getSection(unit_qty_section)
        unit_qty_img=screenshot(section=unit_qty_section,gray=True)
        
        unit_qty_text=read(unit_qty_img, numbers=True)
        
        try:
            unitQty=int(unit_qty_text)
            print(unitQty)
        except ValueError:
            i-=1
            y_correction+=1
            print("Unit qty is not a number")
            continue
            
        #TODO Debug
        cv2.imshow("Unit qty", unit_qty_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    break