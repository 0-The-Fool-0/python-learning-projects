def bind_events(canvas):
    canvas.bind("<Button-1>", on_left_click)
    canvas.bind("<Key>", on_key_press)

def on_left_click(event):
    print(f"Клик по координатам: {event.x}, {event.y}")

def on_key_press(event):
    print(f"Клавиша: {event.keysym}")
