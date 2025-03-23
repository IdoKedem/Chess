import pygame
from game_classes import all_pieces, sprites
from base_classes import Piece
import logistics

class Window:
    def __init__(self, width=600, height=600,
                 board_color="Gray", square_marker_color='Red'):
        pygame.init()
        self.board_color = board_color
        self.square_marker_color = square_marker_color

        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Chess by Ido Kedem")

        self.board = pygame.image.load(f'../Sprites/Boards/{self.board_color}Board.jpg').convert()
        self.square_marker = pygame.image.load(f'../Sprites/SquareMarkers/{self.square_marker_color}.png').convert()

        self.stop_game = False
    def draw_window(self):
        self.window.blit(self.board, (0, 0))

        for piece in all_pieces:
            coords = piece.x, piece.y
            self.window.blit(sprites[piece], coords)
        pygame.display.update()
    def mark_legal_squares(self, piece: Piece):
        # self.window.blit(self.square_marker, (0,0))
        # print('done')
        for square in piece.legal_squares:
            self.window.blit(self.square_marker, (square.x, square.y))
        pygame.display.update()

game_window = Window(width=600, height=600, board_color='Gray')

while not game_window.stop_game:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_window.stop_game = True

    mouse_events = pygame.mouse.get_pressed()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if not 0 < mouse_x < 600:
        continue
    if not 0 < mouse_y < 600:
        continue

    dragged_piece: Piece = logistics.get_dragged_piece()

    if dragged_piece:
        if mouse_events[0]:
            logistics.drag(dragged_piece)
            game_window.mark_legal_squares(dragged_piece)
        else:
            logistics.move_piece(dragged_piece)

    game_window.draw_window()

pygame.quit()




