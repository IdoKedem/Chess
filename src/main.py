import pygame
import logistics


def run():

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return True

    mouse_events = pygame.mouse.get_pressed()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if not 0 < mouse_x < 600:
        return
    if not 0 < mouse_y < 600:
        return

    dragged_piece = logistics.get_dragged_piece()

    if mouse_events[0]:
        logistics.drag(dragged_piece)
    else:
        #for event in events:
        #if event.type == pygame.MOUSEBUTTONUP:

        if dragged_piece:
            logistics.move_piece(dragged_piece)
    return