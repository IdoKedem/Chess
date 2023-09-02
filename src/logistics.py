import pygame
import game_classes
from game_classes import Piece, all_pieces


cur_turn = 1
def get_dragged_piece():
    if any(filter(lambda piece: piece.is_dragged, all_pieces)):  # if there is already a dragged piece
        return get_cur_dragged_piece()

    touched_square = pieces.get_touched_square()
    #print("touched square", touched_square)

    for piece in all_pieces:
        #print(all_pieces)
        if touched_square.occupied_by is piece \
        or piece.is_dragged:
            if piece.color == cur_turn:
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

    desired_square = pieces.get_touched_square()
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
            pieces.remove_piece(occupied_by)


    piece.square.occupied_by = None

    print(f"moving {piece} to {desired_square}")
    globals()['cur_turn'] = int(not cur_turn)  # change global variable

    piece.square = desired_square

    piece.x, piece.y = desired_square.x, desired_square.y

    desired_square.occupied_by = piece

    pieces.update_legal_moves()


