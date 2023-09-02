import pygame
import game_classes
from game_classes import  \
    Piece, all_pieces, all_squares, Square, \
    white_player, black_player


cur_turn_player = white_player
players = [black_player, white_player]
def get_dragged_piece():
    if any(filter(lambda piece: piece.is_dragged, all_pieces)):  # if there is already a dragged piece
        return get_cur_dragged_piece()

    touched_square = get_touched_square()
    #print("touched square", touched_square)

    for piece in all_pieces:
        #print(all_pieces)
        if touched_square.occupied_by is piece \
        or piece.is_dragged:
            if piece.color == cur_turn_player.color:
                piece.is_dragged = True
                return piece


def get_cur_dragged_piece():
    for piece in all_pieces:
        if piece.is_dragged:
            return piece

def drag(piece: Piece):
    if not piece:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()
    piece.x = mouse_x - piece.width / 2
    piece.y = mouse_y - piece.height / 2

    #print("dragging!")



def move_piece(piece: Piece):
    if not piece:
        return

    piece.is_dragged = False

    desired_square = get_touched_square()
    if desired_square not in piece.legal_squares:
        piece.x, piece.y = piece.square.x, piece.square.y
        return

    occupied_by = desired_square.occupied_by

    if occupied_by:
        if occupied_by.color == piece.color or occupied_by is piece:
            #print("cant take your own piece")
            piece.x, piece.y = piece.square.x, piece.square.y
            return
        else:
            game_classes.remove_piece(occupied_by)


    piece.square.occupied_by = None

    print(f"moving {piece} to {desired_square}")
    globals()['cur_turn_player'] = players[
        int(not cur_turn_player.color)]  # change player's turn

    piece.square = desired_square

    piece.x, piece.y = desired_square.x, desired_square.y

    desired_square.occupied_by = piece

    game_classes.update_legal_moves()


def get_touched_square():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    index = Square.get_coords_by_xy(mouse_x, mouse_y)
    #print(mouse_x)
    #print(mouse_y)

    #print(index)

    return all_squares[index]
