
import tkinter as tk
from gui import GameWindow

def main():
    root = tk.Tk()
    app = GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
