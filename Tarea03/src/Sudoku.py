import numpy as np
import random
import math
from typing import List, Tuple
from collections import Counter
import time

class Sudoku:
    def __init__(self, grid):
        self.grid = np.array(grid, dtype=int)       # Copia del tablero inicial
        self.size = self.grid.shape[0]              # n tamaño del sudoku (n x n)

        self.block_size = int(math.sqrt(self.size)) # Tamaño de bloque k = sqrt(n)
        if self.block_size ** 2 != self.size:
            raise ValueError(f"La dimensión {self.size} no es un cuadrado perfecto")

        self.fixed_cells = (self.grid != 0)

    @classmethod
    def from_file(cls, filename):
        file = open(filename,'r')
        lines = [line.strip() for line in file.readlines() if line.strip()]

        grid = []
        for line in lines:
            row = [int(x) for x in line.split()]
            grid.append(row)

        return cls(grid)

    def __str__(self):
        return str(self.grid)

class SudokuSolution:
    def __init__(self, problem):
        self.problem = problem

        # Obtener posiciones de celdas vacías (ordenadas por fila, luego columna)
        self.empty_positions = []
        for i in range(problem.size):
            for j in range(problem.size):
                if not problem.fixed_cells[i, j]:
                    self.empty_positions.append((i, j))
        self.num_empty = len(self.empty_positions)      # Numero de celdas vacías
        self.position_to_index = {pos: idx for idx, pos in enumerate(self.empty_positions)}

        self.values = self._generate_random_solution()

    # Generar solución aleatoria
    def _generate_random_solution(self):
        return [random.randint(1, self.problem.size) for _ in range(self.num_empty)]

    def get_value(self, row, col):
        if self.problem.fixed_cells[row, col]:
            return self.problem.grid[row, col]
        else:
            idx = self.position_to_index[(row, col)]
            return self.values[idx]

    def set_value(self, row, col, value):
        if self.problem.fixed_cells[row, col]:
            raise ValueError(f"No se puede modificar celda fija en ({row}, {col})")

        idx = self.empty_positions.index((row, col))
        self.values[idx] = value

    def get_row(self, row):
        return [self.get_value(row, col) for col in range(self.problem.size)]

    def get_column(self, col):
        return [self.get_value(row, col) for row in range(self.problem.size)]

    def get_block(self, block_row, block_col):
        values = []
        start_row = block_row * self.problem.block_size
        start_col = block_col * self.problem.block_size

        for i in range(start_row, start_row + self.problem.block_size):
            for j in range(start_col, start_col + self.problem.block_size):
                values.append(self.get_value(i, j))

        return values

    def get_grid(self):
        grid = self.problem.grid.copy()

        for idx, (row, col) in enumerate(self.empty_positions):
            grid[row, col] = self.values[idx]

        return grid

    # FUNCIÓN DE EVALUACIÓN
    def evaluate(self):
        """
        Función de evaluación que cuenta el número total de colisiones.
            f(S) = C_filas(S) + C_columnas(S) + C_bloques(S)
        """
        n = self.problem.size
        k = self.problem.block_size
        total_conflicts = 0

        # 1. Colisiones en filas
        for row in range(n):
            values = self.get_row(row)
            total_conflicts += self._count_conflicts_in_group(values)

        # 2. Colisiones en columnas
        for col in range(n):
            values = self.get_column(col)
            total_conflicts += self._count_conflicts_in_group(values)

        # 3. Colisiones en bloques
        for block_row in range(k):
            for block_col in range(k):
                values = self.get_block(block_row, block_col)
                total_conflicts += self._count_conflicts_in_group(values)

        return float(total_conflicts)

    def _count_conflicts_in_group(self, values):
        """
        Cuenta colisiones en un grupo usando conteo de frecuencias.

        1. Contar frecuencia de cada valor
        2. Colisiones = Σ(frecuencia - 1)
        """
        freq = Counter(values)
        return sum(max(0, count - 1) for count in freq.values())

def analyze_representation(problem):
    """Analiza las características de la representación."""
    total_cells = problem.size ** 2
    fixed_cells = np.sum(problem.fixed_cells)
    empty_cells = total_cells - fixed_cells

    return {
        'dimension': f"{problem.size}x{problem.size}",
        'block_size': f"{problem.block_size}x{problem.block_size}",
        'total_cells': total_cells,
        'fixed_cells': int(fixed_cells),
        'empty_cells': int(empty_cells),
        'representation_size': int(empty_cells),
        'reduction_factor': round(total_cells / empty_cells, 2) if empty_cells > 0 else 0,
        'fill_percentage': round((fixed_cells / total_cells) * 100, 2)
    }

def run(problem, num_samples=100):

    results = {}

    fitness_values = []
    generation_times = []

    for _ in range(num_samples):
        start_time = time.time()

        solution = SudokuSolution(problem)
        solution.values = solution._generate_random_solution()

        generation_time = time.time() - start_time
        fitness = solution.evaluate()

        fitness_values.append(fitness)
        generation_times.append(generation_time)

        results = {
            'avg_fitness': np.mean(fitness_values),
            'std_fitness': np.std(fitness_values),
            'min_fitness': np.min(fitness_values),
            'max_fitness': np.max(fitness_values),
            'avg_time': np.mean(generation_times),
            'std_time': np.std(generation_times)
        }

    return results

def create_test_file():
    sudoku_example = """0 5 2 0 0 0 0 1 4
8 0 1 0 9 0 2 0 0
0 0 7 4 0 0 0 8 9
1 2 0 0 8 0 6 3 0
0 0 0 1 0 6 0 0 0
0 6 4 0 7 0 0 5 8
5 1 0 0 0 7 4 0 0
0 0 6 0 5 0 7 0 1
2 7 0 0 0 0 8 9 0"""

    f = open("sudoku_example.txt", "w")
    f.write(sudoku_example)

    return "sudoku_example.txt"

def main():
    """Función principal de demostración."""
    print("=== SISTEMA COMPLETO DE SUDOKU ===\n")

    # Crear archivo de prueba
    filename = create_test_file()
    print(f"Archivo de prueba creado: {filename}")

    # EJERCICIO 1B - Cargar problema
    print("\n--- EJERCICIO 1B: LECTURA DE EJEMPLARES ---")
    problem = Sudoku.from_file(filename)

    # Análisis del problema
    analysis = analyze_representation(problem)
    print(f"Dimensión: {analysis['dimension']}")
    print(f"Tamaño de bloque: {analysis['block_size']}")
    print(f"Celdas totales: {analysis['total_cells']}")
    print(f"Celdas fijas: {analysis['fixed_cells']}")
    print(f"Celdas vacías: {analysis['empty_cells']}")
    print(f"Factor de reducción: {analysis['reduction_factor']}x")
    print(f"Porcentaje completado: {analysis['fill_percentage']}%")

    # EJERCICIO 2A - Representación de soluciones
    print("\n--- EJERCICIO 2A: REPRESENTACIÓN DE SOLUCIONES ---")
    solution = SudokuSolution(problem)
    print(f"Solución creada: {solution}")
    print(f"Representación: vector de {len(solution.values)} elementos")
    print(f"Primeros 10 valores: {solution.values[:10]}")

    # EJERCICIO 2B - Función de evaluación
    print("\n--- EJERCICIO 2B: FUNCIÓN DE EVALUACIÓN ---")
    fitness = solution.evaluate()
    block = solution.get_block(1,2)
    print(f"Fitness inicial: {fitness} colisiones")
    print(f"Block (1,2): {block}")
    full_grid = solution.get_grid()
    for row in full_grid:
        print(' '.join(f'{x:2d}' for x in row))

    row_conflicts = sum(solution._count_conflicts_in_group(solution.get_row(r)) 
                       for r in range(problem.size))
    col_conflicts = sum(solution._count_conflicts_in_group(solution.get_column(c)) 
                       for c in range(problem.size))
    block_conflicts = sum(solution._count_conflicts_in_group(
                         solution.get_block(br, bc))
                         for br in range(problem.block_size) 
                         for bc in range(problem.block_size))

    print(f"  - Colisiones en filas: {row_conflicts}")
    print(f"  - Colisiones en columnas: {col_conflicts}")
    print(f"  - Colisiones en bloques: {block_conflicts}")
    print(f"  - Total: {row_conflicts + col_conflicts + block_conflicts}")

    # EJERCICIO 2C - Generación de soluciones aleatorias
    print("\n--- EJERCICIO 2C: GENERACIÓN DE SOLUCIONES ALEATORIAS ---")
    result = run(problem, 120)

    print(f"{'Fitness Prom.':<12} {'Fitness Min.':<12} {'Tiempo (ms)':<12}")
    print("-" * 60)


    print(f"{result['avg_fitness']:<12.1f} "
          f"{result['min_fitness']:<12.1f} {result['avg_time']*1000:<12.2f}")

    # Mostrar matriz de una solución
    print(f"\nMatriz de solución con fitness {fitness}:")
    grid = solution.get_grid()
    for row in grid:
        print(' '.join(f'{x:2d}' for x in row))

if __name__ == "__main__":
    main()
