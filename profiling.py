from tic_tac_toe_MVC import AI, Model
import timeit


def generate_board(n):
    ai = AI()
    board = Model()
    for i in range(n):
        row, col = ai.choose_random(board)
        board.change_square(row, col, ai.player_num)
        ai.player_num = ai.player_num ^ 3
    return board


if __name__ == '__main__':
    n = 9
    repeat = 100
    lst_random = []
    lst_minimax = []
    for i in range(n):
        ai = AI()
        total_time = 0
        total_time1 = 0
        for j in range(repeat):
            board = generate_board(i)
            #total_time += timeit.timeit(stmt="ai.choose_random(board)", number=10000, globals=globals()) / 10000
            total_time1 += timeit.timeit(stmt="ai.find_best_move(board)", number=50, globals=globals()) / 50
        lst_random.append(round(total_time / repeat * 1000, 6))
        lst_minimax.append(round(total_time1 / repeat * 1000, 6))
    print(lst_random)
    print(lst_minimax)
