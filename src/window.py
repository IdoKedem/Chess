import pygame
import pieces
import main

pygame.init()

board_color = "Gray"

width = 600
height = 600

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess by Ido Kedem")

board = pygame.image.load(f'../Sprites/Boards/{board_color}Board.jpg').convert()

squares = pieces.all_squares

white_pieces = pieces.white_pieces
black_pieces = pieces.black_pieces

all_pieces = pieces.all_pieces

stop_game = False


def draw_window():
    window.blit(board, (0, 0))

    for piece in all_pieces:
        coords = piece.x, piece.y
        window.blit(pieces.sprites[piece], coords)
    pygame.display.update()



while not stop_game:

    stop_game = main.run()
    #print(f"run game is {stop_game}")
    draw_window()


pygame.quit()




