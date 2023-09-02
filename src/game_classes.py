from base_classes import Square, Piece, all_squares
import pygame



class Pawn(Piece):

    @staticmethod
    def get_movement(piece):
        #TODO add en passant logic
        legal_squares = set()

        squares_to_check = 1
        if piece.color == 1:
            y_change = -75
            if piece.square.coord[1] == '2':  # on second rank
                squares_to_check = 2
        else:
            y_change = 75
            if piece.square.coord[1] == '7':  # on 7th rank
                squares_to_check = 2

        for square_num in range(1, squares_to_check + 1):
            cur_square_coords = Square.get_coords_by_xy(piece.square.x,
                                                 piece.square.y + y_change * square_num)
            cur_square = all_squares[cur_square_coords]

            if square_num == 1:  # check takes
                if piece.x != 7 * 75: #not on h file
                    east_square_coords = Square.get_coords_by_xy(cur_square.x + 75, cur_square.y)
                    east_square = all_squares[east_square_coords]
                    if east_square.occupied_by \
                    and east_square.occupied_by.color != piece.color:
                        legal_squares.add(east_square)

                if piece.x != 0: #not on a file
                    west_square_coords = Square.get_coords_by_xy(cur_square.x - 75, cur_square.y)
                    west_square = all_squares[west_square_coords]
                    if west_square.occupied_by \
                    and west_square.occupied_by.color != piece.color:
                        legal_squares.add(west_square)

                if cur_square.occupied_by: # back to checking movement
                    break
            if not cur_square.occupied_by:
                legal_squares.add(cur_square)
        return legal_squares

    def __init__(self, color: int, square: Square):
        super().__init__(color, "pawn", square)
        self.diagonally_legal_squares = set()

    def update_legal_squares(self):
        self.legal_squares = set()

        all_legal_squares = self.get_movement(self)

        self.legal_squares.update(all_legal_squares)
        for square in self.legal_squares:
            if square.x != self.x:  # is diagonal to me
                self.diagonally_legal_squares.add(square)

        print(*self.diagonally_legal_squares)


class Rook(Piece):

    @staticmethod
    def get_movement(piece, direction: str):
        """
        returns a set of legal moves for a rook in a given direction
        :param piece: the piece
        :param direction: in which direction to check
        :return: set of legal moves
        """
        legal_squares = set()

        square_x = piece.x
        square_y = piece.y

        is_check_row = False

        match direction:
            case 'w':
                squares_range_x = range(square_x - 75, -1 * 75, -1 * 75)
                is_check_row = True
            case 'e':
                squares_range_x = range(square_x + 75, 8 * 75, 75)
                is_check_row = True
            case 's':
                squares_range_y = range(square_y + 75, 8 * 75, 75)
            case 'n':
                squares_range_y = range(square_y - 75, -1 * 75, -1 * 75)
            case _:
                raise ValueError("direction must be 'n', 's', 'e' or 'w'")

        if is_check_row:
            for cur_square_x in squares_range_x:
                cur_square_coords = Square.get_coords_by_xy(cur_square_x, square_y)
                cur_square = all_squares[cur_square_coords]

                if cur_square.occupied_by:
                    if cur_square.occupied_by.color != piece.color:
                        legal_squares.add(cur_square)
                    break
                legal_squares.add(cur_square)
        else:
            for cur_square_y in squares_range_y:
                cur_square_coords = Square.get_coords_by_xy(square_x, cur_square_y)
                cur_square = all_squares[cur_square_coords]

                if cur_square.occupied_by:
                    if cur_square.occupied_by.color != piece.color:
                        legal_squares.add(cur_square)
                    break
                legal_squares.add(cur_square)
        return legal_squares


    def __init__(self, color: int, square: Square):
        super().__init__(color, "rook", square)


    def update_legal_squares(self):
        self.legal_squares = set()
        directions = ('n', 's', 'e', 'w')

        for direction in directions:
            self.legal_squares.update(self.get_movement(self, direction))
        #print(*self.legal_squares)


class Bishop(Piece):
    @staticmethod
    def get_movement(piece, direction: str):
        """
        returns a set of legal moves for a piece in a given direction
        :param piece: the piece
        :param direction: in which direction to check
        :return: set of legal moves
        """
        legal_squares = set()

        square_x, square_y = piece.x, piece.y

        match direction:
            case 'nw':
                slope = 1
                squares_range_x = range(square_x - 75, -1 * 75, -1 * 75)
            case 'ne':
                slope = -1
                squares_range_x = range(square_x + 75, 8 * 75, 75)
            case 'sw':
                slope = -1
                squares_range_x = range(square_x - 75, -1 * 75, -1 * 75)
            case 'se':
                slope = 1
                squares_range_x = range(square_x + 75, 8 * 75, 75)
            case _:
                raise ValueError("direction must be 'nw', 'ne', 'sw' or 'se'")

        for cur_square_x in squares_range_x:
            cur_square_y = slope * (cur_square_x - square_x) + square_y

            square_coord = Square.get_coords_by_xy(cur_square_x, cur_square_y)
            if square_coord not in all_squares.keys():
                break
            square = all_squares[square_coord]
            if square.occupied_by:
                if square.occupied_by.color != piece.color:
                    legal_squares.add(square)
                break
            legal_squares.add(square)

        return legal_squares


    def __init__(self, color: int, square: Square):
        super().__init__(color, "bishop", square)

    def update_legal_squares(self):
        self.legal_squares = set()

        directions = ('nw', 'ne', 'sw', 'se')
        for direction in directions:
            self.legal_squares.update(self.get_movement(self, direction))


class Knight(Piece):

    @staticmethod
    def get_movement(piece, direction: str):
        """
        returns a set of legal moves for a piece in a given direction
        for the knight, this checks the squares that are two squares to a direction, and its two adjacent squares
        :param piece: the piece
        :param direction: in which direction to check
        :return: set of legal moves
        """
        legal_squares = set()

        check_x_axis = False
        possible_squares = set()

        match direction:
            case 'n':
                square_x = piece.square.x
                square_y = piece.square.y - 2 * 75
            case 's':
                square_x = piece.square.x
                square_y = piece.square.y + 2 * 75
            case 'e':
                check_x_axis = True
                square_x = piece.square.x + 2 * 75
                square_y = piece.square.y
            case 'w':
                check_x_axis = True
                square_x = piece.square.x - 2 * 75
                square_y = piece.square.y
            case _:
                raise ValueError("direction must be 'n', 's', 'e' or 'w'")

        if check_x_axis:
            possible_squares.add(Square.get_coords_by_xy(square_x, square_y + 75))
            possible_squares.add(Square.get_coords_by_xy(square_x, square_y - 75))
        else:
            possible_squares.add(Square.get_coords_by_xy(square_x + 75, square_y))
            possible_squares.add(Square.get_coords_by_xy(square_x - 75, square_y))

        for square in possible_squares:
            if square in all_squares:
                legal_squares.add(all_squares[square])
        return legal_squares


    def __init__(self, color, square):
        super().__init__(color, 'Knight', square)

    def update_legal_squares(self):
        self.legal_squares = set()

        directions = ('n', 's', 'e', 'w')
        for direction in directions:
            self.legal_squares.update(self.get_movement(self, direction))
        #print(*self.legal_squares)

class King(Piece):
    @staticmethod
    def get_movement(piece, direction: str):
        """
        returns a set of legal moves for a piece in a given direction
        for the king, returns the 3 possible squares it can go to in a given direction
        DOES NOT TAKE INTO ACCOUNT SQUARES ENEMY PIECES SEE

        :param piece: the piece
        :param direction: the direction to check in
        :return: set of legal moves
        """
        legal_squares = set()
        possible_squares = set()

        check_x_axis = False

        match direction:
            case 'n':
                square_x = piece.square.x
                square_y = piece.square.y - 75 # select square above
            case 's':
                square_x = piece.square.x
                square_y = piece.square.y + 75 # select square below
            case 'e':
                check_x_axis = True
                square_x = piece.square.x + 75 # select square to the right
                square_y = piece.square.y
            case 'w':
                check_x_axis = True
                square_x = piece.square.x - 75 # select square to the left
                square_y = piece.square.y
            case _:
                raise ValueError("direction must be 'n', 's', 'e' or 'w'")

        if check_x_axis:
            for y_change in range(-1, 2):
                square_coords = Square.get_coords_by_xy(square_x, square_y + 75 * y_change)
                if square_coords in all_squares:
                    possible_squares.add(all_squares[square_coords])
        else:
            for x_change in range(-1, 2):
                square_coords = Square.get_coords_by_xy(square_x + 75 * x_change, square_y)
                if square_coords in all_squares:
                    possible_squares.add(all_squares[square_coords])

        for square in possible_squares:
            if square in all_squares.values():
                if square.occupied_by:
                    if square.occupied_by.color == piece.color:
                        continue
                legal_squares.add(square)

        return legal_squares



    def __init__(self, color, square):
        super().__init__(color, 'king', square)

    def update_legal_squares(self):
        self.legal_squares = set()

        directions = ('n', 'e', 'w', 's')
        for direction in directions:
            self.legal_squares.update(self.get_movement(self, direction))

        #print("possible squares")
        #print(*self.legal_squares)

        for piece in all_pieces:
            if piece.color == self.color:
                continue
            if type(piece) == Pawn: # SPECIAL CASE: only check for diagonal legal squares
                to_remove = piece.diagonally_legal_squares
            else:
                to_remove = piece.legal_squares

            if self.legal_squares.intersection(to_remove): # enemy piece controls a possible square
                self.legal_squares.difference_update(to_remove) # remove overlapping squares


        #print("filtered squares:")
        #print(*self.legal_squares)
        #print("-------")

class Queen(Piece):
    def __init__(self, color, square):
        super().__init__(color, "queen", square)

    @staticmethod
    def get_movement(piece, direction: str):
        legal_squares = set()

        if len(direction) == 1: # n, e, s or w
            legal_squares.update(Rook.get_movement(piece, direction))
        else:  #ne, nw, se, sw
            legal_squares.update(Bishop.get_movement(piece, direction))
        return legal_squares

    def update_legal_squares(self):
        self.legal_squares = set()

        directions = ('n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw')
        for direction in directions:
            self.legal_squares.update(self.get_movement(self, direction))

        #print("queem legal ssquares")
        #print(*self.legal_squares)


class Player:
    def __init__(self, name: str, color: int):
        self.name = name
        self.color = color

        if color == 1:  # white
            self.pieces = [
                Rook(1, all_squares['a4']),
                Bishop(1, all_squares['b4']),
                King(1, all_squares['b5'])
            ]
        else:  # black
            self.pieces = [
                Knight(0, all_squares['g4']),
                Pawn(0, all_squares['g7']),
                Queen(0, all_squares['d5'])
            ]


white_player = Player(name="White", color=1)
black_player = Player(name="Black", color=0)

white_pieces = white_player.pieces
black_pieces = black_player.pieces
all_pieces = white_pieces + black_pieces

def update_legal_moves():
    for piece in all_pieces:
            piece.update_legal_squares()

update_legal_moves()



sprites = {}
for piece in all_pieces:
    sprites[piece] = pygame.image.load(piece.sprite)

def remove_piece(piece):
    if piece.color == 1:
        white_pieces.remove(piece)
    else:
        black_pieces.remove(piece)
    all_pieces.remove(piece)

    del sprites[piece]
    print("removed")






