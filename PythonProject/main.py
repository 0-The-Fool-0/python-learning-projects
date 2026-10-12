
import tkinter as tk
from gui import GameWindow
import logic
from graphics import GameCanvas

def main():
    root = tk.Tk()
    app = GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()