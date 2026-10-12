import tkinter as tk
from PIL import Image, ImageTk

class GameCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.bind("<Button-3>", self.show_context_menu)
        self.draw_grid()
        self.images = {}

    def draw_grid(self):
        size = 50
        for i in range(8):
            for j in range(8):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                self.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=color)

    def load_image(self, name, path, x, y):
        img = Image.open(path)
        self.images[name] = ImageTk.PhotoImage(img)
        self.create_image(x, y, image=self.images[name], anchor='nw')

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Отменить ход")
        menu.post(event.x_root, event.y_root)
