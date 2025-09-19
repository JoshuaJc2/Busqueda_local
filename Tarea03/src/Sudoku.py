import numpy as np
import math

class Sudoku:
    def __init__(self, grid):
        self.grid = np.array(grid, dtype=int)           # Matriz del ejemplar de sudoku
        self.size = self.grid.shape[0]                  # Dimensión n = k^2
        self.block_size = int(math.sqrt(self.size))     # Tamaño k de un bloque

        # Máscara de celdas fijas (True = fijo, False = vacío)
        self.fixed_cells = (self.grid != 0)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        grid = []
        for line in lines:
            row = [int(x) for x in line.split()]
            grid.append(row)

        return cls(grid)

    def __str__(self):
        return str(self.grid)

if __name__ == "__main__":
    # prueba
    sudoku = """0 5 2 0 0 0 0 1 4
8 0 1 0 9 0 2 0 0
0 0 7 4 0 0 0 8 9
1 2 0 0 8 0 6 3 0
0 0 0 1 0 6 0 0 0
0 6 4 0 7 0 0 5 8
5 1 0 0 0 7 4 0 0
0 0 6 0 5 0 7 0 1
2 7 0 0 0 0 8 9 0"""

    with open("sudoku_test.txt", "w") as f:
        f.write(sudoku)

    problem = Sudoku.from_file("sudoku_test.txt")
    print(problem.grid)
    print(f"Dimensión: {problem.size}x{problem.size}")
    print(f"Tamaño de bloque: {problem.block_size}x{problem.block_size}")
    print(f"Celdas fijas: {np.sum(problem.fixed_cells)}")
    print(f"Celdas vacías: {np.sum(~problem.fixed_cells)}")
