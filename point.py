# Refer to README.md

class Point:
    # Point class for organization of needed positions
    direction = 0

    def __init__(self, x: int, y: int, direction: int):
        self.__x = x
        self.__y = y
        self.direction = direction

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_direction(self):
        return self.direction

    def get_four_options(self) -> []:
        # Get options for inputs
        up = optional_points(0, self)
        right = optional_points(1, self)
        down = optional_points(2, self)
        left = optional_points(3, self)
        return [up, right, down, left]


def optional_points(choice: int, option) -> Point:
    # Provide optional points of movement based on direction
    if choice == 0:  # Up
        return Point(option.get_x(), option.get_y() + 1, choice)
    if choice == 1:  # Right
        return Point(option.get_x() + 1, option.get_y(), choice)
    if choice == 2:  # Down
        return Point(option.get_x(), option.get_y() - 1, choice)
    if choice == 3:  # Left
        return Point(option.get_x() - 1, option.get_y(), choice)
