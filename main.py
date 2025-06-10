from functools import partial
import tkinter as tk
from itertools import cycle, product
from tkinter import *
from tkinter import messagebox

DEFAULT_HIGHLIGHT_COLOR = "MediumPurple2"
ACTIVE_HIGHLIGHT_COLOR = "SeaGreen2"

class Player():
    def __init__(self, name:str, icon:str = "x"):
        self.name = name
        self.icon = icon
        self.moves_idx = {k: [] for k in range(9)}

    def add_move(self, ultimate_idx, simple_idx):
        print("ultimate_idx, simple_idx", ultimate_idx, simple_idx)
        print(self.moves_idx[ultimate_idx])
        self.moves_idx[ultimate_idx] += [simple_idx]

class UltimateGame():
    def __init__(self, root):
        self.players = [Player("sonia", "O"), Player("marcelo", "X")]
        self.players_cycle = cycle(self.players)
        self.current_player = next(self.players_cycle)

        mainFrame = Frame(root)
        mainFrame.pack( side = LEFT, pady=20, padx=20 )

        self.simple_games = []

        for x in range(3):
            for y in range(3):
                simple_game = SimpleGame(mainFrame, row=x, column=y, ultimate_game=self)
                self.simple_games.append(simple_game)

        bottomFrame = Frame(root)
        bottomFrame.pack( side = RIGHT )

        self.clear_button = tk.Label(bottomFrame, text="Clear screen", width=10, font=("", 10), bd=3,
                                relief="groove")
        self.clear_button.pack()
        self.clear_button.bind("<Button-1>", self.clear)

    def clear(self, event):
        for button in self.buttons:
            button.config(text="")

    def selectNextSimpleGame(self, button_idx):
        self.simple_games[button_idx].mainFrame.configure(highlightbackground=ACTIVE_HIGHLIGHT_COLOR)


class SimpleGame():
    def __init__(self, root, row, column, ultimate_game):
        self.ultimate_game = ultimate_game
        self.buttons = []
        self.mainFrame = Frame(root, highlightbackground=DEFAULT_HIGHLIGHT_COLOR, highlightthickness=2)
        self.mainFrame.grid(row=row, column=column, pady=1, padx=1)
        self.game_idx = (row * 3) + column  

        for x in range(3):
            for y in range(3):
                button = tk.Label(self.mainFrame, text="", width=3, height=1, font=("", 25), bd=1,
                                relief="groove")

                button.grid(row=x, column=y)

                command = partial(self.move, button)
                button.bind("<Button-1>", command)
                self.buttons.append(button)
        
    def move(self, button, event):
        button_idx = self.buttons.index(button)
        print(button_idx)
        # Only if the button is empty
        if button.cget("text") == "":
            button.config(text=self.ultimate_game.current_player.icon)
            self.ultimate_game.current_player.add_move(self.game_idx, button_idx)
            self.check_game_status()
            self.ultimate_game.current_player = next(self.ultimate_game.players_cycle)
            self.ultimate_game.selectNextSimpleGame(button_idx)
            self.mainFrame.configure(highlightbackground=DEFAULT_HIGHLIGHT_COLOR)
    
    def check_game_status(self):
        # TODO: check for wins and ties
        print("check_game_status")
        for player in self.ultimate_game.players:
            won = self.won(player)
            print(player.name, "has won? ", won)
            if won:
                messagebox.showinfo("Congratulations!", f"{player.name} WON!") 

    def won(self, player):
        player.moves_idx[self.game_idx].sort()
        print(player.moves_idx)
        
        # rows logic
        for init_idx in [0, 3, 6]:
            winning_idxs = [init_idx, init_idx +1 , init_idx + 2]
            if set(winning_idxs).issubset(player.moves_idx[self.game_idx]):
                return True

        # column logic
        for init_idx in [0, 1, 2]:
            winning_idxs = [init_idx, init_idx +2 , init_idx + 4]
            if set(winning_idxs).issubset(player.moves_idx[self.game_idx]):
                return True

        # positive diagonal
        init_idx = 0
        winning_idxs = [init_idx, init_idx + 4 , init_idx + 8]
        if set(winning_idxs).issubset(player.moves_idx[self.game_idx]):
            return True

        # negative diagonal
        init_idx = 2
        winning_idxs = [init_idx, init_idx + 2 , init_idx + 4]
        if set(winning_idxs).issubset(player.moves_idx[self.game_idx]):
            return True

        return False


def main():
    root = tk.Tk()
    root.title('Ultimate Tic Tac Toe')

    UltimateGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
