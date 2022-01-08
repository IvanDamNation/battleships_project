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


# Constructing ship with dot objects
class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orient = orientation
        self.hp = length

    @property
    def ship_dots(self):
        ship_placement = []
        for hull in range(self.length):
            current_x = self.bow.x
            current_y = self.bow.y

            if self.orient == 0:
                current_x += hull

            elif self.orient == 1:
                current_y += hull

            ship_placement.append(Dot(current_x, current_y))

        return ship_placement

    def get_hit(self, shot):
        return shot in self.ship_dots
