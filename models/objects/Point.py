class Point:

    def __init__(self, x=0, y=0, relative=False):
        self.x = x
        self.y = y
        self.relative = relative
        self.coordinates = [x, y]


    def __add__(self, other):
        if isinstance(other, tuple):
            if len(other) != len(self.coordinates):
                raise ValueError("Tuple dimensions must match Point dimensions")

            x, y = other[0],other[1]

        elif isinstance(other, Point):
            if not (not self.relative and other.relative):
                raise ValueError("Only a relative point can be added to an absolute point")

            x, y = other.x, other.y

        else:
            raise TypeError("Unsupported operand type(s) for +: 'Point' and '{}'".format(type(other)))

        return Point(self.x + x, self.y + y)

    def __getitem__(self, key):
        return self.coordinates[key]

    def __str__(self):
        return f"({self.x}, {self.y}, rel: {self.relative})"

    def __repr__(self):
        return self.__str__()
