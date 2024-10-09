import mss
import numpy as np
import util
from common import AttackPanel



nth =0
width=23


def take(nth:int):
    nth_point=AttackPanel.nth_commander_point(nth)

    # this 35+20 is extremely sensitive, even if you change it only by one pixel
    # tesseract won't be able to recognize it
    global height

    number_section=(
        nth_point.x,nth_point.y,
        width+50,30+height
    )

    section = util.getSection(number_section)
    return  util.screenshot(section)

#
#
# screenshot =take(1)
#
# import cv2
# gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
# _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
#
# th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY,11,-11)
#
# from config import TesseractConfig
# text=util.read(binary_image,TesseractConfig.default().With(":"))
# print(text)
#
# util.showImg(binary_image)
# exit()
#
# test= np.arange(6).reshape(3,2)
# print(test)
# exit()






import cv2
def getdiff(imgA:np.ndarray,imgB:np.ndarray):
    assert imgA.shape == imgB.shape,"The shape of the images must match"

    total=0
    for x in range(imgA.shape[1]):
        for y in range(imgA.shape[0]):
            ...


print((np.subtract( [68,51,38],[189 ,182, 157])**2).sum())
#45_963

def test(nth):
    A =take(nth)
    B=take(2)

    white=0
    A = np.insert(A,[23]*200,white,axis=1)

    A = np.delete(A,np.s_[23::],axis=1)
    A = np.insert(A,[23]*20,A[1,1],axis=1)
    # A = cv2.cvtColor(A,cv2.COLOR_RGB2GRAY)
    from config import TesseractConfig
    config = TesseractConfig.number_optimized()
    config.psm_=13
    text= util.read(A,config)
    print(text)
    # util.showImg(A)
    # exit()

global height
height=20
# test(4)
# exit()
for i in range(7):
    test(i)

exit()


bg_color = [189 ,182, 157]
font_color = [68 ,51, 38]

colors=[]
count=0
for y in range(A.shape[0]):
    bin=""
    for x in range(A.shape[1]):
        # if A[y,x] != [189 ,182, 157]:
        if (np.subtract( A[y,x],font_color)**2).sum() < 1000:
            # print(f"{y},{x}")
            # print(A[y,x])
            # exit()
            colors.append(A[y,x])
            count+=1
            bin+="0"
        else:
            bin+="."
    print(bin)

print(count)
# for c in colors:
#     print(c)


exit()
thresh = getdiff(A, B)
total=A.shape[0]*A.shape[1]
diff = cv2.countNonZero(thresh)

print(diff/total)

