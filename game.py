# Refer to README.md

import random

from point import Point


class Game:
    max_x = 12
    max_y = 12
    board = []
    body = []
    direction = 0
    target = None
    score = 0
    won = False
    lose = False
    ate = False
    move_count = 0
    total_move_count = 0
    head = Point(0, 0, 0)
    MAX_SCORE = (max_x - 2) * (max_y - 2) - 2

    def __init__(self):
        # Fill board with zeroes
        for i in range(self.max_y):
            new = []
            for j in range(self.max_x):
                if i == 0 or i == self.max_x - 1 or j == 0 or j == self.max_y - 1:
                    new.append(3)
                else:
                    new.append(0)
            self.board.append(new)

        self.direction = 0
        # Append first 2 locations of snake to body
        self.body.append(Point(1, 1, self.direction))
        self.body.append(Point(1, 2, self.direction))
        # Save head
        self.head = self.body[-1]
        # Show tail of snake on board
        self.board[1][1] = 1
        # Show head of snake
        self.board[1][2] = 1
        # Show and define target
        self.relocate_target()

    def reset(self):
        # Reset game
        self.board = []
        self.body = []
        self.score = 0
        self.won = False
        self.lose = False
        self.ate = False
        self.move_count = 0
        self.total_move_count = 0
        self.__init__()

    def print_board(self):
        # Match for x and y coordinates
        for i in range(self.max_x - 1, - 1, -1):
            for j in range(self.max_y):
                print(self.board[j][i], end='')
            print()
        print()

    def move(self, choice):
        # Update direction based on choice
        self.direction = choice
        self.total_move_count += 1
        self.move_count += 1
        if self.move_count > ((self.max_y - 2) * (self.max_x - 2)):
            self.lose = True
            return

        # Adjust point to next position
        if self.direction == 0:  # Up
            self.head = Point(self.head.get_x(), (self.head.get_y() + 1), self.direction)
        elif self.direction == 1:  # Right
            self.head = Point((self.head.get_x() + 1), self.head.get_y(), self.direction)
        elif self.direction == 2:  # Down
            self.head = Point(self.head.get_x(), (self.head.get_y() - 1), self.direction)
        else:  # Left
            self.head = Point((self.head.get_x() - 1), self.head.get_y(), self.direction)

        # Pop body if didn't eat last round
        if not self.ate:
            # Pop tail on body and save point
            tail = self.body.pop(0)
            # Update board to popped tail
            self.board[tail.get_x()][tail.get_y()] = 0
        else:
            # Reset ate Boolean and move_count if ate
            self.ate = False
            self.move_count = 0

        # Running into body or wall
        if self.board[self.head.get_x()][self.head.get_y()] == 1 or \
                self.board[self.head.get_x()][self.head.get_y()] == 3:
            # End game with lose Boolean
            self.lose = True
            return

        # Check if won
        self.won = (self.score == self.MAX_SCORE)

        # Check if ate and adjust accordingly
        if self.board[self.head.get_x()][self.head.get_y()] == 2:
            self.score += 1
            if not self.won:
                self.relocate_target()
            self.ate = True

        # If survived, append head position on body
        self.body.append(self.head)
        self.board[self.head.get_x()][self.head.get_y()] = 1

        # Return score if won
        if self.won:
            return self.score

    def relocate_target(self):
        # Find a 0 location for next target
        point = Point(random.randint(0, self.max_x - 1), random.randint(0, self.max_y - 1), self.direction)
        while self.board[point.get_x()][point.get_y()] != 0:
            point = Point(random.randint(0, self.max_x - 1), random.randint(0, self.max_y - 1), self.direction)
        # Update board
        self.board[point.get_x()][point.get_y()] = 2
        # Update target
        self.target = point


current_game = Game()
