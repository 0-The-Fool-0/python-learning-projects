# gui.py (пример фрагмента для прорисовки)
class GameWindow:
    def __init__(self, root):
        self.root = root
        self.canvas = GameCanvas(root)
        self.game_logic = GameLogic(10, 10)
        self.cell_size = 50
        self._setup_controls()
        self._setup_canvas()
        self._load_images()

    def _setup_canvas(self):
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    def _on_canvas_click(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if self.game_logic.add_point(x, y):
            self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_points()

    def _draw_points(self):
        for player, points in self.game_logic.player_points.items():
            color = 'blue' if player == 1 else 'red'
            for (x, y) in points:
                self.canvas.create_oval(
                    x*self.cell_size+10, y*self.cell_size+10,
                    (x+1)*self.cell_size-10, (y+1)*self.cell_size-10,
                    fill=color
                )
def _setup_controls(self):
    self.root.bind("<Up>", lambda e: self.game_logic.move_selected('up'))
    self.root.bind("<Down>", lambda e: self.game_logic.move_selected('down'))
    self.root.bind("<Left>", lambda e: self.game_logic.move_selected('left'))
    self.root.bind("<Right>", lambda e: self.game_logic.move_selected('right'))
    self.root.bind("<Escape>", lambda e: self._reset_selection())