
class FlankSide:
    @staticmethod
    def right():
        return FlankSide("right")
    @staticmethod
    def left():
        return FlankSide("left")

    def __init__(self, side):
        self._side =side

    def __eq__(self, other):
        return self._side == other._side
