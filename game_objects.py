# file contains objects definition for Battleships game

# base object
class Dot:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def __eq__(self, other):  # Comparing shortcut
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # Print shortcut
        return f'Dot({self.x}, {self.y})'
