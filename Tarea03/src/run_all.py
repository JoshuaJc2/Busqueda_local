import os
import subprocess

ejemplares = [
    "Ejemplares/David_Filmer1.txt",
    "Ejemplares/Easy1.txt",
    "Ejemplares/Hard1.txt",
    "Ejemplares/Medium1.txt",
    "Ejemplares/SD2.txt"
]

metodos = ['g', 's', 'l']  # geometric, slow, linear
repeticiones = 10
output_file = "resultados.txt"

with open(output_file, 'w') as f:
    for ejemplar in ejemplares:
        for metodo in metodos:
            f.write(f"Ejemplar: {os.path.basename(ejemplar)}, Método: {metodo}\n")
            for i in range(repeticiones):
                # Ejecuta el sudoku.py con el ejemplar y método de enfriamiento
                result = subprocess.run(
                    ["python3", "sudoku.py", ejemplar, metodo],
                    capture_output=True, text=True
                )

                # Extrae solo fitness final y número de iteraciones
                lines = result.stdout.splitlines()
                fitness_line = next((l for l in lines if "Fitness final" in l), "Fitness final: N/A")
                iterations_line = next((l for l in lines if "Iteraciones" in l), "Iteraciones: N/A")

                f.write(f"Repetición {i+1}: {fitness_line}, {iterations_line}\n")
            f.write("\n")
