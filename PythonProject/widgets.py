from tkinter import Entry, Button, Scale, HORIZONTAL, StringVar, OptionMenu, ttk

def build_controls(root, canvas):
    entry = Entry(root)
    entry.pack()

    def on_click():
        text = entry.get()
        print("Введено:", text)

    Button(root, text="Считать", command=on_click).pack()

    Scale(root, from_=1, to=10, orient=HORIZONTAL).pack()

    options = ["тонкая", "средняя", "толстая"]
    var = StringVar(root)
    var.set(options[0])
    OptionMenu(root, var, *options).pack()

    tree = ttk.Treeview(root, columns=("A", "B"), show='headings')
    tree.heading("A", text="Игрок")
    tree.heading("B", text="Очки")
    tree.insert("", "end", values=("Игрок1", 5))
    tree.pack()
