# file contains objects definition for Battleships game

# Exceptions section
class BoardException(Exception):
    pass


class OutOfRangeException(BoardException):
    def __str__(self):
        return 'Coordinates out of board range.'


class UsedCoordinatesException(BoardException):
    def __str__(self):
        return 'You already shoot on this coordinate.'


class WrongShipPlacement(BoardException):
    pass


# base object
class Dot:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def __eq__(self, other):  # Comparing shortcut
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # Print shortcut
        return f'Dot({self.x}, {self.y})'
