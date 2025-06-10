from functools import partial
import tkinter as tk
from itertools import cycle

class Player():
    def __init__(self, icon:str = "x"):
        self.icon = icon


class SimpleGame():
    def __init__(self, root):
        self.players = [Player("O"), Player("X")]
        self.players_cycle = cycle(self.players)
        self.current_player = next(self.players_cycle)

        self.buttons = []

        for x in range(3):
            for y in range(3):
                button = tk.Label(root, text="", width=3, font=("", 25), bd=1,
                                relief="groove")

                button.grid(row=x, column=y)

                command = partial(self.move, button)
                button.bind("<Button-1>", command)
                self.buttons.append(button)

        self.clear_button = tk.Label(root, text="Clear screen", width=3, font=("", 15), bd=3,
                                relief="groove")
        self.clear_button.grid(row=4, column=0, columnspan=3, sticky="news")

        self.clear_button.bind("<Button-1>", self.clear) # Left click
                

    def move(self, button, event):
        # Only if the button is empty
        if button.cget("text") == "":
            button.config(text=self.current_player.icon)
            self.current_player = next(self.players_cycle)

    def clear(self, event):
        for button in self.buttons:
            button.config(text="")

def main():
    root = tk.Tk()
    SimpleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
