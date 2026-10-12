import unittest
from logic import is_valid_move
import unittest
from logic import GameLogic

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Создаем игровую логику с полем 10x10 для каждого теста
        self.game = GameLogic(10, 10)

    def test_initialization(self):
        # Проверяем начальное состояние игры
        self.assertEqual(self.game.size_x, 10)
        self.assertEqual(self.game.size_y, 10)
        self.assertEqual(len(self.game.dots), 0)
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(self.game.scores, {1: 0, 2: 0})

    def test_add_dot(self):
        # Проверяем добавление точки
        result = self.game.add_dot(5, 5)
        self.assertTrue(result)
        self.assertIn((5, 5), self.game.dots)
        self.assertEqual(self.game.current_player, 2)  # Ход должен перейти ко второму игроку

    def test_add_duplicate_dot(self):
        # Проверяем что нельзя добавить точку в занятую клетку
        self.game.add_dot(5, 5)
        result = self.game.add_dot(5, 5)
        self.assertFalse(result)
        # Текущий игрок не должен измениться после неудачного хода
        self.assertEqual(self.game.current_player, 2)

    def test_add_out_of_bounds(self):
        # Проверяем что нельзя добавить точку за пределами поля
        self.assertFalse(self.game.is_valid_move(-1, 5))
        self.assertFalse(self.game.is_valid_move(5, -1))
        self.assertFalse(self.game.is_valid_move(10, 5))
        self.assertFalse(self.game.is_valid_move(5, 10))

    def test_clear_board(self):
        # Проверяем очистку доски
        self.game.add_dot(5, 5)
        self.game.add_dot(6, 6)
        self.game.clear_board()
        self.assertEqual(len(self.game.dots), 0)

    def test_win_horizontal(self):
        # Проверяем выигрыш по горизонтали
        self.game.add_dot(3, 5)  # Игрок 1
        self.assertEqual(self.game.scores[1], 0)

        self.game.add_dot(3, 6)  # Игрок 2
        self.game.add_dot(4, 5)  # Игрок 1
        self.game.add_dot(4, 6)  # Игрок 2
        self.game.add_dot(5, 5)  # Игрок 1 - выигрышный ход (3 в ряд)

        # Проверяем, что очки начислены игроку 1
        self.assertEqual(self.game.scores[1], 1)
        self.assertEqual(self.game.scores[2], 0)

    def test_reset_scores(self):
        # Проверяем сброс счета
        self.game.scores = {1: 5, 2: 3}
        self.game.reset_scores()
        self.assertEqual(self.game.scores, {1: 0, 2: 0})

if __name__ == '__main__':
    unittest.main()
class TestLogic(unittest.TestCase):
    def test_move(self):
        self.assertTrue(is_valid_move("pawn", (1, 1), (2, 1)))
        self.assertFalse(is_valid_move("pawn", (2, 2), (2, 2)))

if __name__ == '__main__':
    unittest.main()
