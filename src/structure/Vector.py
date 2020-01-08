from copy import copy


class Vector2:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.y = y
        self.x = x

    def copy(self):
        return copy(self)

    def asTuple(self) -> (int, int):
        return self.x, self.y

    def asTupleWithArgs(self, args: tuple):
        return self.asTuple() + args

    def __str__(self):
        return f"(x:{self.x}, y:{self.y})"

    def __truediv__(self, other):
        return Vector2(self.x // other.x, self.y // other.y)

    def __mul__(self, other):
        return Vector2(self.x * other.x, self.y * other.y)



if __name__ == '__main__':
    test = Vector2(8, 32) / Vector2(2, 4)
    print(test.x)
    print(test.y)
