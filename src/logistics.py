import pygame
import game_classes
from game_classes import  \
    Piece, all_pieces, all_squares, Square, \
    Player, players_list
from typing import List


cur_turn_player: Player = players_list[1] # white



def get_dragged_piece() -> Piece:
    if any(filter(lambda piece: piece.is_dragged, all_pieces)):  # if there is already a dragged piece
        return get_cur_dragged_piece()

    touched_square = get_touched_square()
    #print("touched square", touched_square)

    for piece in all_pieces:
        #print(all_pieces)
        if not(
           touched_square.occupied_by is piece or piece.is_dragged):
            continue

        if piece.color != cur_turn_player.color:
            continue

        piece.is_dragged = True
        return piece


def get_cur_dragged_piece():
    for piece in all_pieces:
        if piece.is_dragged:
            return piece

def drag(piece: Piece):

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

    occupying_piece = desired_square.occupied_by

    if occupying_piece:
        if occupying_piece.color == piece.color or occupying_piece is piece:
            #print("cant take your own piece")
            piece.x, piece.y = piece.square.x, piece.square.y
            return
        else:
            game_classes.remove_piece(occupying_piece)

    piece.square.occupied_by = None

    print(f"moving {piece} to {desired_square}")

    last_turn_player = cur_turn_player
    globals()['cur_turn_player']: Player = \
        players_list[
        int(not cur_turn_player.color)]  # change player's turn

    piece.square = desired_square
    piece.x, piece.y = desired_square.x, desired_square.y
    desired_square.occupied_by = piece

    game_classes.update_legal_moves([last_turn_player])
    look_for_checks(last_turn_player=last_turn_player,
                    cur_turn_player=cur_turn_player)


def get_touched_square():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    index = Square.get_coords_by_xy(mouse_x, mouse_y)
    #print(mouse_x)
    #print(mouse_y)

    #print(index)

    return all_squares[index]

def look_for_checks(last_turn_player, cur_turn_player):
    cur_turn_player.is_in_check = \
        cur_turn_player.king in \
        last_turn_player.all_legal_squares
    game_classes.update_legal_moves([cur_turn_player])
