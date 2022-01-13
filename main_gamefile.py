# This is a main file of "Battleships" game.
# Gameplay in Python Console only (for now).
# 'AI' is primitive (just random)

# Made for final practice exercise in chapter
# "OOP" for SkillFactory

# For education purpose only. Workability is not guarantee.

# Made by IvanDamNation (a.k.a. IDN)
# GNU General Public License v3, 2022


# Import section
from random import randint

from game_objects import BoardException, OutOfRange, UsedCoordinates, \
    WrongShipPlacement
from game_objects import Dot, Ship, GameField, Human, AI

# For more options info look in "options.py" file
# from options import WIDTH, SHIP_LIST  # TODO Uncomment in future


class MainGameObject:
    def __init__(self, width=6):
        self.width = width
        player_board = self.make_board_forced()
        computer_board = self.make_board_forced()
        computer_board.hidden = True

        self.ai = AI(computer_board, player_board)
        self.user = Human(player_board, computer_board)

    def make_board(self):  # TODO Make ship lengths changeable
        lengths = [3, 2, 2, 1, 1, 1, 1]
        board = GameField()
        attempt_count = 0
        for taken_length in lengths:
            while True:
                attempt_count += 1
                if attempt_count > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.width),
                                randint(0, self.width)),
                            taken_length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except WrongShipPlacement:
                    pass
        board.clean_used_dots()
        return board

    def make_board_forced(self):
        board = None
        while board is None:
            board = self.make_board()
        return board

    def rules(self):
        print('Welcome to the Battleships game!')
        print('--------------------------------------')
        print('The rules are standard.')
        print('Input X and Y coordinates for shoot.')
        print("Try to hit all opponent's ships on map")
        print('before opponent destroy all yours.')
        print('Your opponent will be simple AI.')
        print('--------------------------------------')
        print('Good luck!')

    def party_cycle(self):
        move = 0
        while True:
            print('-' * 20)
            print('User board.')
            print(self.user.board)
            print('-' * 20)
            print('AI board.')
            print(self.ai.board)
            print('-' * 20)
            if move % 2 == 0:
                print('User move:')
                new_shot = self.user.move()
            else:
                print('Computer move:')
                new_shot = self.ai.move()
            if not new_shot:
                move -= 1  # For same player move when get hit

            if self.ai.board.destroyed == 7:
                print('-' * 20)
                print('You win!')
                break

            if self.user.board.destroyed == 7:
                print('-' * 20)
                print('Computer win!')
                break

    def open_game(self):
        self.rules()
        self.party_cycle()


# Starting section
if __name__ == '__main__':
    game = MainGameObject()
    game.open_game()
    # print(game.make_board_forced())
