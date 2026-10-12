import tkinter as tk

from logic import GameLogic


class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Dots — coursework prototype")
        self.game_logic = GameLogic(10, 10)
        self.cell_size = 50
        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status, anchor="w").pack(fill=tk.X)
        self.canvas = tk.Canvas(
            root,
            width=self.game_logic.size_x * self.cell_size,
            height=self.game_logic.size_y * self.cell_size,
            background="white",
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        tk.Button(root, text="New game", command=self._reset).pack(pady=6)
        self._redraw()

    def _on_canvas_click(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if self.game_logic.add_point(x, y):
            self._redraw()

    def _reset(self):
        self.game_logic.clear_board()
        self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        width = self.game_logic.size_x * self.cell_size
        height = self.game_logic.size_y * self.cell_size
        for x in range(self.game_logic.size_x + 1):
            px = x * self.cell_size
            self.canvas.create_line(px, 0, px, height, fill="#cccccc")
        for y in range(self.game_logic.size_y + 1):
            py = y * self.cell_size
            self.canvas.create_line(0, py, width, py, fill="#cccccc")

        colors = {1: "#2563eb", 2: "#dc2626"}
        for player, points in self.game_logic.player_points.items():
            for (x, y) in points:
                inset = self.cell_size * 0.2
                self.canvas.create_oval(
                    x * self.cell_size + inset,
                    y * self.cell_size + inset,
                    (x + 1) * self.cell_size - inset,
                    (y + 1) * self.cell_size - inset,
                    fill=colors[player],
                    outline="",
                )

        self.status.set(
            f"Player {self.game_logic.current_player} to move — "
            f"scores: {self.game_logic.scores[1]}–{self.game_logic.scores[2]}"
        )
