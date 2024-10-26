from typing import Callable

class ClickStep:
    def __init__(self,movement:Callable,onStepComplete:Callable=None):
        self.movement = movement
        self.onStepComplete = onStepComplete


    def play(self):

        self.movement()

        if self.onStepComplete is not None:
            self.onStepComplete()


