import pygame
import numpy
import random
import logging

logging.basicConfig(level=logging.DEBUG)

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


class AI:
    # level 0 - random ai
    # level 1 - unbeatable ai
    def __init__(self, level=0, player_num=2):
        self.level = level
        self.player_num = player_num

    # choose random empty square
    @staticmethod
    def choose_random(board):
        empty_squares = board.get_empty_squares()
        i = random.randint(0, len(empty_squares) - 1)
        return empty_squares[i]

    # minimax to choose best moves
    def minimax(self, board, maximizing):
        # ai wins
        if board.is_winner(self.player_num):
            return 1

        # player wins
        if board.is_winner(self.player_num ^ 3):
            return -1

        # draw
        if board.is_board_full():
            return 0

        if maximizing:
            best_score = -1000
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares:
                board.change_square(row, col, self.player_num)
                score = self.minimax(board, False)
                board.undo(row, col)
                if score > best_score:
                    best_score = score
            return best_score
        else:
            best_score = 1000
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares:
                board.change_square(row, col, self.player_num ^ 3)
                score = self.minimax(board, True)
                board.undo(row, col)
                if score < best_score:
                    best_score = score
            return best_score

    def find_best_move(self, board):
        best_score = -1000
        for (row, col) in board.get_empty_squares():
            board.change_square(row, col, self.player_num)
            score = self.minimax(board, False)
            board.undo(row, col)
            if score > best_score:
                best_score = score
                row_best, col_best = (row, col)
        return row_best, col_best

    # decide how to act depending on level
    def choose_pos(self, board):
        if self.level == 0:
            return self.choose_random(board)
        else:
            return self.find_best_move(board)


class Model:

    def __init__(self):
        self.board = numpy.zeros((N, N))

    def change_square(self, row, col, player):
        self.board[row][col] = player

    def undo(self, row, col):
        self.board[row][col] = 0

    def is_empty_square(self, row, col):
        return self.board[row][col] == 0

    def get_empty_squares(self):
        lst = []
        for row in range(N):
            for col in range(N):
                if self.is_empty_square(row, col):
                    lst.append((row, col))
        return lst

    def is_board_full(self):
        for row in range(N):
            for col in range(N):
                if self.board[row][col] == 0:
                    return False
        return True

    def is_winner(self, player_num):
        for col in range(N):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player_num:
                return True
        for row in range(N):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == player_num:
                return True

        if self.board[2][0] == self.board[1][1] == self.board[0][2] == player_num:
            return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player_num:
            return True
        return False


class View:

    @staticmethod
    def draw_figures(board):
        for row in range(N):
            for col in range(N):
                if board.board[row][col] == 1:
                    pygame.draw.circle(surface, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                       row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, LINE_WIDTH)
                if board.board[row][col] == 2:
                    pygame.draw.line(surface, RED,
                                     (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE + SQUARE_SIZE - MARGIN),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - MARGIN, row * SQUARE_SIZE + MARGIN), LINE_WIDTH)
                    pygame.draw.line(surface, RED, (col * SQUARE_SIZE + MARGIN, row * SQUARE_SIZE + MARGIN),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - MARGIN,
                                      row * SQUARE_SIZE + SQUARE_SIZE - MARGIN),
                                     LINE_WIDTH)

    @staticmethod
    def draw_winning_lines(board):
        for col in range(N):
            if board.board[0][col] == board.board[1][col] == board.board[2][col] and board.board[0][col] != 0:
                pygame.draw.line(surface, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 15),
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 15), LINE_WIDTH)

        for row in range(N):
            if board.board[row][0] == board.board[row][1] == board.board[row][2] and board.board[row][0] != 0:
                pygame.draw.line(surface, RED, (15, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                 (WIDTH - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2), LINE_WIDTH)

        if board.board[2][0] == board.board[1][1] == board.board[0][2] and board.board[2][0] != 0:
            pygame.draw.line(surface, RED, (MARGIN // 2, HEIGHT - MARGIN // 2),
                             (WIDTH - MARGIN // 2, MARGIN // 2), LINE_WIDTH)

        if board.board[0][0] == board.board[1][1] == board.board[2][2] and board.board[0][0] != 0:
            pygame.draw.line(surface, RED, (MARGIN // 2, MARGIN // 2),
                             (WIDTH - MARGIN // 2, HEIGHT - MARGIN // 2), LINE_WIDTH)

    @staticmethod
    def draw_board():
        surface.fill(GREY)
        # draw horizontal lines
        pygame.draw.line(surface, BLACK, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(surface, BLACK, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        # draw vertical lines
        pygame.draw.line(surface, BLACK, (SQUARE_SIZE, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH)
        pygame.draw.line(surface, BLACK, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


class Controller:

    def __init__(self):
        self.board = Model()
        self.view = View()
        self.ai = AI()
        self.mode = 0  # 0 - vs Player, 1 - vs AI
        self.player_num = 1

    def restart(self):
        self.view.draw_board()
        self.__init__()
        logging.debug("PVP on")

    def change_mode(self):
        self.mode = self.mode ^ 1
        if self.mode == 0:
            self.change_ai(0)
            logging.debug("PVP on")
        else:
            logging.debug("AI on")

    def change_ai(self, level):
        self.ai.level = level
        if level == 1:
            logging.debug("unbeatable AI on")
        else:
            logging.debug("random AI on")

    def is_over(self):
        return self.board.is_winner(1) or self.board.is_winner(2) or self.board.is_board_full()

    def make_move(self, row, col):
        self.board.change_square(row, col, self.player_num)
        self.player_num = self.player_num ^ 3


def main():
    game = Controller()
    game.restart()
    ai = game.ai
    board = game.board

    running = True
    while running:
        for event in pygame.event.get():
            # event handler for pressing keys
            if event.type == pygame.KEYDOWN:
                # change the game mode if 'c' is pressed
                if event.key == pygame.K_c:
                    game.change_mode()
                # restart the game if 'r' is pressed
                if event.key == pygame.K_r:
                    game.restart()
                    ai = game.ai
                    board = game.board
                # change to random AI
                if event.key == pygame.K_0:
                    game.change_ai(0)
                # change to unbeatable AI
                if event.key == pygame.K_1:
                    game.change_ai(1)
            # click event
            if not game.is_over() and event.type == pygame.MOUSEBUTTONDOWN:
                # get coordinates of mouse click
                x, y = pygame.mouse.get_pos()
                # get column and row of mouse click
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if board.is_empty_square(row, col):
                    game.make_move(row, col)
                    game.view.draw_figures(board)
                    if game.is_over():
                        game.view.draw_winning_lines(board)
            # AI making move event
            if not game.is_over() and game.player_num == ai.player_num and game.mode == 1:
                pygame.display.update()
                row, col = ai.choose_pos(board)

                game.make_move(row, col)
                game.view.draw_figures(board)
                if game.is_over():
                    game.view.draw_winning_lines(board)

            # event handler to handle quitting the application
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


if __name__ == '__main__':
    main()
