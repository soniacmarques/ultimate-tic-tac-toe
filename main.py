from functools import partial
import tkinter as tk
from itertools import cycle

class Player():
    def __init__(self, name:str, icon:str = "x"):
        self.name = name
        self.icon = icon
        self.moves_idx = []

    def add_move(self, index):
        self.moves_idx.append(index)



class SimpleGame():
    def __init__(self, root):
        self.players = [Player("sonia", "O"), Player("marcelo", "X")]
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
        button_idx = self.buttons.index(button)
        print(button_idx)
        # Only if the button is empty
        if button.cget("text") == "":
            button.config(text=self.current_player.icon)
            self.current_player.add_move(button_idx)
            self.check_game_status()
            self.current_player = next(self.players_cycle)
        
    
    def check_game_status(self):
        # TODO: check for wins and ties
        print("check_game_status")
        for player in self.players:
            won = self.won(player)
            print(player.name, "has won? ", won)

    def won(self, player):
        player.moves_idx.sort()
        print(player.moves_idx)
        
        # rows logic
        for init_idx in [0, 3, 6]:
            winning_idxs = [init_idx, init_idx +1 , init_idx + 2]
            if set(winning_idxs).issubset(player.moves_idx):
                return True

        # column logic
        for init_idx in [0, 1, 2]:
            winning_idxs = [init_idx, init_idx +2 , init_idx + 4]
            if set(winning_idxs).issubset(player.moves_idx):
                return True

        # positive diagonal
        init_idx = 0
        winning_idxs = [init_idx, init_idx + 4 , init_idx + 8]
        if set(winning_idxs).issubset(player.moves_idx):
            return True

        # negative diagonal
        init_idx = 2
        winning_idxs = [init_idx, init_idx + 2 , init_idx + 4]
        if set(winning_idxs).issubset(player.moves_idx):
            return True

        return False

    def clear(self, event):
        for button in self.buttons:
            button.config(text="")

def main():
    root = tk.Tk()
    SimpleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
