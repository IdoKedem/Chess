class Square:
    width, height = 75, 75

    def __init__(self, x, y, coord: str, occupied_by=None):
        self.x = x
        self.y = y
        self.coord = coord

        self.occupied_by = occupied_by

    def __str__(self):
        return self.coord



def get_squares():
    x, y = 0, 0
    squares = {}

    for letter in range(ord('a'), ord('h') + 1):
        for num in range(8, 0, -1):
            index = chr(letter) + str(num)
            squares[index] = (Square(x, y, index))

            y += Square.height
        y = 0
        x += Square.width
    return {index: squares[index] for index in sorted(squares.keys())}

all_squares = get_squares()



def get_coords_by_xy(x, y):
    letter = x // Square.width
    number = 8 - y // Square.height

    index = chr(ord('a') + letter) + str(number)
    return index
