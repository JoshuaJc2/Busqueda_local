import numpy as np
import random
import math
from typing import List, Tuple
from collections import Counter
import time
import os
import sys

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
    def __init__(self, problem, values=None):
        self.problem = problem

        # Obtener posiciones de celdas vacías
        self.empty_positions = []
        for i in range(problem.size):
            for j in range(problem.size):
                if not problem.fixed_cells[i, j]:
                    self.empty_positions.append((i, j))
        self.num_empty = len(self.empty_positions)      # Numero de celdas vacías
        self.position_to_index = {pos: idx for idx, pos in enumerate(self.empty_positions)}

        if values is not None:
            if len(values) != self.num_empty:
                raise ValueError(f"Se esperaban {self.num_empty} valores, se recibieron {len(values)}")
            self.values = list(values)
        else:
            self.values = self._generate_random_solution()

    def _generate_random_solution(self):
        n = self.problem.size

        # Contar valores fijos en el tablero
        fixed_counts = Counter()
        for i in range(n):
            for j in range(n):
                if self.problem.fixed_cells[i, j]:
                    value = self.problem.grid[i, j]
                    fixed_counts[value] += 1

        # Calcular cuántos de cada valor necesitamos agregar
        needed_counts = {}
        for value in range(1, n + 1):
            current_count = fixed_counts.get(value, 0)
            needed = n - current_count
            needed_counts[value] = needed

        # Crear lista de valores necesarios para completar
        values_needed = []
        for value, count in needed_counts.items():
            values_needed.extend([value] * count)

        # Mezclar aleatoriamente los valores necesarios
        random.shuffle(values_needed)

        return values_needed

    def get_value(self, row, col):
        if self.problem.fixed_cells[row, col]:
            return self.problem.grid[row, col]
        else:
            idx = self.position_to_index[(row, col)]
            return self.values[idx]

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

    def evaluate(self):
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
        freq = Counter(values)
        return sum(max(0, count - 1) for count in freq.values())

    def copy(self):
        return SudokuSolution(self.problem, self.values.copy())

    def get_neighbor(self):
        if self.num_empty < 2:
            return self.copy()
        # Crear copia de la solución actual
        neighbor = self.copy()
        idx1, idx2 = random.sample(range(self.num_empty), 2)

        neighbor.values[idx1], neighbor.values[idx2] = neighbor.values[idx2], neighbor.values[idx1]
        return neighbor


def geometric_cooling(current_temperature, alpha):
    return alpha * current_temperature

def slow_cooling(current_temperature, alpha):
    return  (current_temperature/(1+alpha*current_temperature))

def simulated_annealing(problem, initial_temp=100.0, alpha=0.85, N0_factor = 2, p=1.15, max_iteration = 250000, cooling_func='g'):
    # Inicialización
    current_solution = SudokuSolution(problem)
    current_fitness = current_solution.evaluate()
    best_solution = current_solution.copy()
    best_fitness = current_fitness

    N = int(N0_factor * problem.size)
    temperature = initial_temp
    iteration = 0

    print(f"Temperatura inicial: {temperature}")
    # Ciclo principal
    while temperature > 1e-4 and best_fitness > 0 and iteration < max_iteration:
        for _ in range(N):
            # Generar vecino
            neighbor = current_solution.get_neighbor()
            neighbor_fitness = neighbor.evaluate()

            delta_fitness = neighbor_fitness - current_fitness
            if delta_fitness <= 0:
                accept = True
            else:
                probability = math.exp(-delta_fitness / temperature)
                accept = random.random() < probability

            # Actualizar solución actual
            if accept:
                current_solution = neighbor
                current_fitness = neighbor_fitness

                # Actualizar mejor solución
                if current_fitness < best_fitness:
                    best_solution = current_solution.copy()
                    best_fitness = current_fitness

            print("Data")
            print(best_fitness)
            print(iteration)
            print(temperature)
            iteration += 1
        if cooling_func== 'g':
            temperature = geometric_cooling(temperature, alpha)
        elif cooling_func=='s':
            temperature = slow_cooling(temperature, alpha)
        N = int(N * p)

    print(f"Iteraciones: {iteration}")
    return best_solution, best_fitness


def solve_sudoku_from_file(filename, alpha=0.85, cooling_func='g'):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"El archivo '{filename}' no fue encontrado")
    try:
        problem = Sudoku.from_file(filename)

        # Calcular temperatura inicial basada en el problema
        sample_solution = SudokuSolution(problem)
        initial_fitness = sample_solution.evaluate()
        initial_temp = initial_fitness * 0.5

        # Ejecutar recocido simulado
        if cooling_func == 'g':
            best_solution, best_fitness = simulated_annealing(
                problem=problem,
                initial_temp=initial_temp,
                alpha=0.85,
                cooling_func = 'g',
            )
        elif cooling_func == 's':
            best_solution, best_fitness = simulated_annealing(
                problem=problem,
                initial_temp=initial_temp,
                alpha=0.0005,
                cooling_func = 's',
            )
        else:
            best_solution, best_fitness = simulated_annealing(
                problem=problem,
                initial_temp=initial_temp,
                alpha=alpha,
                cooling_func = geometric_cooling,
            )

        return best_solution

    except Exception as e:
        raise ValueError(f"Error al procesar el archivo '{filename}': {str(e)}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python SimulatedAnnealing.py archivo.txt")
        sys.exit(1)
    filename = sys.argv[1]
    cooling_func = sys.argv[2]

    try:
        print(f"Resolviendo sudoku desde: {filename}")
        print("Ejecutando Recocido Simulado...")

        solution = solve_sudoku_from_file(filename)

        fitness = solution.evaluate()
        print(f"\nResultados:")
        print(f"Fitness final: {fitness}")

        if fitness == 0:
            print("¡SUDOKU RESUELTO!")
        else:
            print("Mejor solución encontrada:")

        grid = solution.get_grid()
        print("\nSolución:")
        for row in grid:
            print(' '.join(f'{x:2d}' for x in row))

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
