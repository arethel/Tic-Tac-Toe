from tic_tac_toe_MVC import Model, N
import unittest
import random


class TestModel(unittest.TestCase):
    def test_change_square(self):
        model = Model()
        for row in range(N):
            for col in range(N):
                number = random.randint(1, 2)
                model.change_square(row, col, number)
                self.assertEqual(model.board[row][col], number)
        self.assertTrue(model.is_board_full())

    def test_is_empty_square(self):
        model = Model()
        for row in range(N):
            for col in range(N):
                number = random.randint(1, 2)
                model.change_square(row, col, number)
                self.assertFalse(model.is_empty_square(row, col))

    def test_is_winner(self):
        model = Model()
        model1 = Model()
        model2 = Model()
        model3 = Model()
        for player in range(1, 3):
            for row in range(N):
                for col in range(N):
                    if row == col:
                        model.change_square(row, col, player)
                    else:
                        model.change_square(row, col, random.randint(1, 2))
                    if row + col == N - 1:
                        model1.change_square(row, col, player)
                    else:
                        model1.change_square(row, col, random.randint(1, 2))
                    if row == 1:
                        model2.change_square(row, col, player)
                    else:
                        model2.change_square(row, col, random.randint(1, 2))
                    if col == 1:
                        model3.change_square(row, col, player)
                    else:
                        model3.change_square(row, col, random.randint(1, 2))
            self.assertTrue(model.is_winner(player))
            self.assertTrue(model1.is_winner(player))
            self.assertTrue(model2.is_winner(player))
            self.assertTrue(model3.is_winner(player))


if __name__ == '__main__':
    unittest.main()
