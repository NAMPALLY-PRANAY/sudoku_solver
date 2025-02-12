import tkinter as tk
from tkinter import messagebox

def create_grid(size):
    for widget in grid_frame.winfo_children():
        widget.destroy()

    entries.clear()
    for i in range(size):
        row_entries = []
        for j in range(size):
            entry = tk.Entry(grid_frame, width=4, font=('Arial', 16), justify='center', bd=1, relief='solid')
            entry.grid(row=i, column=j, padx=1, pady=1, sticky='nsew')
            row_entries.append(entry)
        entries.append(row_entries)
    
    # Configure grid lines for 9x9 with bold lines
    if size == 9:
        for i in range(10):
            if i % 3 == 0:
                grid_frame.grid_rowconfigure(i, weight=1)
                grid_frame.grid_columnconfigure(i, weight=1)
                grid_frame.grid_rowconfigure(i, minsize=2)
                grid_frame.grid_columnconfigure(i, minsize=2)
            else:
                grid_frame.grid_rowconfigure(i, weight=1)
                grid_frame.grid_columnconfigure(i, weight=1)
    
def get_grid_values(size):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            value = entries[i][j].get()
            if value.isdigit():
                row.append(int(value))
            else:
                row.append(0)
        grid.append(row)
    return grid

def set_grid_values(grid):
    size = len(grid)
    for i in range(size):
        for j in range(size):
            entries[i][j].delete(0, tk.END)
            if grid[i][j] != 0:
                entries[i][j].insert(0, grid[i][j])

def is_valid(grid, row, col, num):
    size = len(grid)
    box_size = int(size ** 0.5)
    
    if num in grid[row]:
        return False
    
    if num in [grid[i][col] for i in range(size)]:
        return False
    
    start_row, start_col = row - row % box_size, col - col % box_size
    for i in range(start_row, start_row + box_size):
        for j in range(start_col, start_col + box_size):
            if grid[i][j] == num:
                return False
    return True

def solve(grid):
    size = len(grid)
    box_size = int(size ** 0.5)
    
    for row in range(size):
        for col in range(size):
            if grid[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def on_submit():
    size = int(size_var.get())
    grid = get_grid_values(size)
    if solve(grid):
        set_grid_values(grid)
    else:
        messagebox.showinfo("Result", "No solution exists")

def on_clear():
    size = int(size_var.get())
    for i in range(size):
        for j in range(size):
            entries[i][j].delete(0, tk.END)

app = tk.Tk()
app.title("Sudoku Solver")

size_var = tk.StringVar(value='9')
sizes = ['3', '6', '9', '16']

size_menu = tk.OptionMenu(app, size_var, *sizes, command=lambda _: create_grid(int(size_var.get())))
size_menu.pack(pady=10)

grid_frame = tk.Frame(app)
grid_frame.pack()

entries = []

create_grid(int(size_var.get()))

submit_btn = tk.Button(app, text="Submit", command=on_submit, bg="lightgreen", font=('Arial', 12, 'bold'))
submit_btn.pack(side=tk.LEFT, padx=10, pady=10)

clear_btn = tk.Button(app, text="Clear", command=on_clear, bg="lightcoral", font=('Arial', 12, 'bold'))
clear_btn.pack(side=tk.RIGHT, padx=10, pady=10)

app.mainloop()
