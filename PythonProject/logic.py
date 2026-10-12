# logic.py
class GameLogic:
    def __init__(self, size_x=10, size_y=10):
        self.size_x = size_x
        self.size_y = size_y
        self.player_points = {1: set(), 2: set()}
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.lines = []  # для линий окружения

    def add_point(self, x, y):
        if not self.is_valid_move(x, y):
            return False
        self.player_points[self.current_player].add((x, y))
        self.check_capture(x, y)
        self.current_player = 3 - self.current_player
        return True

    def is_valid_move(self, x, y):
        return (0 <= x < self.size_x and 0 <= y < self.size_y and
                (x, y) not in self.player_points[1] and
                (x, y) not in self.player_points[2])

    def check_capture(self, x, y):
        # Тут реализуем проверку окружения
        opponent = 3 - self.current_player
        enemy_points = self.player_points[opponent]
        for point in list(enemy_points):
            if self.is_point_surrounded(point):
                self.capture_point(point, opponent)

    def is_point_surrounded(self, point):
        # Проверка окружения точки
        # Реализуем алгоритм поиска, например, обход графа
        # Пока оставить как заглушку
        return False

    def capture_point(self, point, opponent):
        self.player_points[opponent].remove(point)
        self.player_points[self.current_player].add(point)
        self.scores[self.current_player] += 1

    def clear_board(self):
        self.player_points = {1: set(), 2: set()}
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
