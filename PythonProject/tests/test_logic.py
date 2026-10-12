import unittest

from logic import GameLogic


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game = GameLogic(10, 10)

    def test_initial_state(self):
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(self.game.player_points, {1: set(), 2: set()})
        self.assertEqual(self.game.scores, {1: 0, 2: 0})

    def test_valid_moves_alternate_players(self):
        self.assertTrue(self.game.add_point(5, 5))
        self.assertIn((5, 5), self.game.player_points[1])
        self.assertEqual(self.game.current_player, 2)

        self.assertTrue(self.game.add_point(6, 5))
        self.assertIn((6, 5), self.game.player_points[2])
        self.assertEqual(self.game.current_player, 1)

    def test_occupied_and_out_of_bounds_moves_are_rejected(self):
        self.assertTrue(self.game.add_point(5, 5))
        self.assertFalse(self.game.add_point(5, 5))
        self.assertFalse(self.game.add_point(-1, 0))
        self.assertFalse(self.game.add_point(0, 10))
        self.assertEqual(self.game.current_player, 2)

    def test_clear_board_resets_points_score_and_turn(self):
        self.game.add_point(5, 5)
        self.game.scores[1] = 3
        self.game.clear_board()

        self.assertEqual(self.game.player_points, {1: set(), 2: set()})
        self.assertEqual(self.game.scores, {1: 0, 2: 0})
        self.assertEqual(self.game.current_player, 1)


if __name__ == "__main__":
    unittest.main()
