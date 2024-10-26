import util
import actions
from resources import symbol as gui



def main():
    popup_section=(1130,710, 30,60)

    section=util.getSection(popup_section)

    img= util.screenshot(section, to_cv2=False)





if __name__ == '__main__':
    import eventloop

    eventloop.wrap(main).wait()