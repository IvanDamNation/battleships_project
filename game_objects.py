# File contains objects definition for Battleships game

# Exceptions section
class BoardException(Exception):
    pass


class OutOfRange(BoardException):
    def __str__(self):
        return 'Coordinates out of board range.'


class UsedCoordinates(BoardException):
    def __str__(self):
        return 'You already shoot on this coordinate.'


class WrongShipPlacement(BoardException):
    pass


# Base object
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
        """
        Initializing
        :param bow: "pointer" dot (zero-index dot)
        :param length: amount of dots in ship
        :param orientation: 0 for horizontal, 1 for vertical
        """
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


# Object for board presentation
class GameField:
    def __init__(self, hidden=False, width=6):
        self.width = width
        self.hidden = hidden

        self.destroyed = 0  # Ship counter

        self.field_itself = [[' '] * width for _ in range(width)]

        self.used_dots = []
        self.ships_on_field = []

    def __str__(self):
        pres = ''
        pres += '\t| ' + \
                ' | '.join(map(str, range(self.width))) + ' |\n'
        pres += '\t' + '----' * self.width + ' \n'

        for col, row in enumerate(self.field_itself):
            pres += f'{col}\t| ' + ' | '.join(row) + ' |\n'

        if self.hidden:
            pres = pres.replace('O', ' ')
        return pres

    def out_of_border(self, dot):
        return not ((0 <= dot.x < self.width) and
                    (0 <= dot.y < self.width))

    def occupy_dots(self, ship, verbose=False):
        adjacent = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 0), (0, 1),
                    (1, -1), (1, 0), (1, 1)]

        for dot in ship.ship_dots:
            for delta_x, delta_y in adjacent:
                new_dot = Dot(dot.x + delta_x, dot.y + delta_y)
                if not (self.out_of_border(new_dot)) and \
                        new_dot not in self.used_dots:
                    if verbose:
                        self.field_itself[new_dot.x][new_dot.y] = '.'

                    self.used_dots.append(new_dot)

    def add_ship(self, ship):
        for dot in ship.ship_dots:
            if self.out_of_border(dot) or dot in self.used_dots:
                raise WrongShipPlacement
        for dot in ship.ship_dots:
            self.field_itself[dot.x][dot.y] = 'O'
            self.used_dots.append(dot)

        self.ships_on_field.append(ship)
        self.occupy_dots(ship)

    def fire(self, dot):
        if self.out_of_border(dot):
            raise OutOfRange()

        if dot in self.used_dots:
            raise UsedCoordinates()

        self.used_dots.append(dot)

        for ship in self.ships_on_field:
            if ship.get_hit(dot):
                ship.hp -= 1
                self.field_itself[dot.x][dot.y] = 'X'
                if ship.hp == 0:
                    self.destroyed += 1
                    self.occupy_dots(ship, verbose=True)
                    print('Ship destroyed!')
                    return False
                else:
                    print('Ship get hit!')
                    return True

        self.field_itself[dot.x][dot.y] = '.'
        print('Missed.')
        return False

    def clean_used_dots(self):
        self.used_dots = []


class PlayerMain:
    def __init__(self, player_board, enemy_board):
        self.board = player_board
        self.enemy = enemy_board

    def get_coord(self):
        raise NotImplementedError()

    def move(self):
        acceptable = False
        new_shot = None

        while not acceptable:
            try:
                target = self.get_coord()
                new_shot = self.enemy.fire(target)
            except BoardException as error:
                print(error)
            else:
                acceptable = True

        return new_shot
