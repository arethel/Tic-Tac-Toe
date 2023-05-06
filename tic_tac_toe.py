import pygame
import numpy

# specify constants to avoid magic numbers
WIDTH, HEIGHT = (420, 420)
N = 3
SQUARE_SIZE = WIDTH // N
LINE_WIDTH = 11
MARGIN = SQUARE_SIZE // 4
CIRCLE_RADIUS = SQUARE_SIZE // 3
# constants for colors
GREY = (160, 160, 160)
BLACK = (18, 18, 18)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.init()
pygame.display.set_caption("Tic Tac Toe")

# establish width and height of window and add color
surface = pygame.display.set_mode((WIDTH, HEIGHT))
surface.fill(GREY)

# internal representation of board
# Empty fields have the value 0
# Fields taken by Player 1 have the value 1
# Fields taken by Player 2 have the value 2
board = numpy.zeros((N, N))


# helper functions to work with board
def change_square(row, col, player_num):
    board[row][col] = player_num


def is_empty_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                return False
    return True


def draw_lines():
    # draw horizontal lines
    pygame.draw.line(surface, BLACK, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(surface, BLACK, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # draw vertical lines
    pygame.draw.line(surface, BLACK, (SQUARE_SIZE, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(surface, BLACK, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(N):
        for col in range(N):
            if board[row][col] == 1:
                pygame.draw.circle(surface, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                   row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, LINE_WIDTH)
            if board[row][col] == 2:
                pygame.draw.line(surface, RED, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE + SQUARE_SIZE - MARGIN),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - MARGIN, row * SQUARE_SIZE + MARGIN), LINE_WIDTH)
                pygame.draw.line(surface, RED, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE + MARGIN),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - MARGIN, row * SQUARE_SIZE + SQUARE_SIZE - MARGIN),
                                 LINE_WIDTH)


def is_winner(player_num):
    for col in range(N):
        if board[0][col] == board[1][col] == board[2][col] == player_num:
            pygame.draw.line(surface, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 15),
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 15), LINE_WIDTH)
            return True
    for row in range(N):
        if board[row][0] == board[row][1] == board[row][2] == player_num:
            pygame.draw.line(surface, RED, (15, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                             (WIDTH - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2), LINE_WIDTH)
            return True

    if board[2][0] == board[1][1] == board[0][2] == player_num:
        pygame.draw.line(surface, RED, (MARGIN // 2, HEIGHT - MARGIN // 2),
                         (WIDTH - MARGIN // 2, MARGIN // 2), LINE_WIDTH)
        return True
    if board[0][0] == board[1][1] == board[2][2] == player_num:
        pygame.draw.line(surface, RED, (MARGIN // 2, MARGIN // 2),
                         (WIDTH - MARGIN // 2, HEIGHT - MARGIN // 2), LINE_WIDTH)
        return True
    return False


def restart():
    surface.fill(GREY)
    draw_lines()
    for row in range(N):
        for col in range(N):
            board[row][col] = 0


def main():
    restart()
    running = True
    player_num = 1
    is_game_over = False

    while running:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and not is_game_over:

                # get coordinates of mouse click
                x, y = pygame.mouse.get_pos()
                # get column and row of mouse click
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if is_empty_square(row, col):
                    change_square(row, col, player_num)

                    if is_winner(player_num) or is_board_full():
                        is_game_over = True
                    player_num = player_num ^ 3

                    draw_figures()

                # restart the game if 'r' is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    running = True
                    is_game_over = False
                    player_num = 1

            # event handler to handle quitting the application
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()


if __name__ == '__main__':
    main()
