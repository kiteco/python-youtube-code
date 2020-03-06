import tkinter as tk
import random
import colors as c
import functions as f


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')

        main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=400, height=400)
        main_grid.grid()
        self.make_GUI(main_grid)
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        self.mainloop()


    def make_GUI(self, main_grid):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(main_grid, width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell_display = tk.Label(cell, width=10, height=5, bg=c.EMPTY_CELL_COLOR, font=c.FONT)
                cell_display.grid()
                row.append(cell_display)
            self.cells.append(row)


    def start_game(self):
        # create matrix of zeroes
        self.matrix = [ [0] * 4 for _ in range(4) ]

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col].configure(bg=c.CELL_COLORS[2], text="2", fg=c.CELL_NUMBER_COLORS[2])
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col].configure(bg=c.CELL_COLORS[2], text="2", fg=c.CELL_NUMBER_COLORS[2])


    # Matrix Manipulation Functions

    def stack(self):
        new_matrix = [ [0] * 4 for _ in range(4) ]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix


    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0


    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix


    def transpose(self):
        new_matrix = [ [0] * 4 for _ in range(4) ]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix


    # Add a 2 tile randomly to an empty cell

    def add_new_2(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2


    # Update the GUI to match the matrix

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j].configure(bg=c.CELL_COLORS[cell_value], text=str(cell_value), fg=c.CELL_NUMBER_COLORS[cell_value])
        self.update_idletasks()


    # Arrow-Press Functions
    
    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_2()
        self.update_grid()

    
    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_2()
        self.update_grid()
    

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_2()
        self.update_grid()
    

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_2()
        self.update_grid()
        


game = Game()
        

