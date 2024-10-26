from utils import mouse
from uielements.gameobject import NomadCamp
from bot import state

import resources.symbol as sym

# exit()
def main():
    camp = NomadCamp((100,100))
    mouse.click(camp)


#
# from uielements.gameobject import Button
#
# b = Button(sym.nomad_individual_reward_popup,(1000,1000))
# print(b.section)
# exit()

if __name__ == "__main__":
    import eventloop
    eventloop.wrap(main).wait()