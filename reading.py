import pytesseract
from PIL import Image
import cv2
import numpy as np

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

screenshot = cv2.imread('test captures/food_1.png', cv2.IMREAD_COLOR)
screen_np = np.array(screenshot)

custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

# Convert the screenshot to grayscale for better OCR
gray_screenshot = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray_screenshot, lang="hun",config=custom_config).strip()

print("Detected text:", text)
