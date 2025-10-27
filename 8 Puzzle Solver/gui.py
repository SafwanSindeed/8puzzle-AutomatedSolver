import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
from solver import solve_puzzle, check_solvable, Goal

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8-Puzzle A* Visualization")

        # Load the same starting state as your solver test case
        self.current_state = "724506831"

        self.buttons = []
        self.is_solving = False  # to prevent multiple concurrent solves

        # Create 3x3 grid of buttons
        for i in range(9):
            btn = tk.Button(master, text="", font=("Helvetica", 24), width=4, height=2, state="disabled")
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Control buttons
        tk.Button(master, text="Randomize", command=self.randomize_board, width=10, height=2, bg="lightblue").grid(row=3, column=0)
        tk.Button(master, text="Solve", command=self.start_solver_thread, width=10, height=2, bg="lightgreen").grid(row=3, column=2)

        # Initialize display
        self.update_board(self.current_state)

    def update_board(self, state):
        for i, val in enumerate(state):
            self.buttons[i].config(text=val if val != '0' else "")
        self.master.update_idletasks()

    def randomize_board(self):
        """Generates a random solvable puzzle"""
        if self.is_solving:
            return  # prevent randomization during solving

        state = list("012345678")
        while True:
            random.shuffle(state)
            state_str = "".join(state)
            if check_solvable(state_str):
                self.current_state = state_str
                break
        self.update_board(self.current_state)

    def start_solver_thread(self):
        """Run solver in a separate thread to prevent GUI freeze"""
        if self.is_solving:
            return
        self.is_solving = True
        threading.Thread(target=self.solve_board, daemon=True).start()

    def solve_board(self):
        start = self.current_state
        path, moves = solve_puzzle(start)

        if not path:
            messagebox.showinfo("8-Puzzle", "This puzzle is not solvable!")
            self.is_solving = False
            return

        for state in path:
            self.update_board(state)
            time.sleep(0.4)  

        messagebox.showinfo("8-Puzzle", f"Solved in {len(moves)} moves!")
        self.is_solving = False


if __name__ == "__main__":
    root = tk.Tk()
    gui = PuzzleGUI(root)
    root.mainloop()
