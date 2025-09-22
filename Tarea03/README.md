# README

**Equipo:** TheKingdomPinguin

## Descripción
Implementación del algoritmo de Recocido Simulado (Simulated Annealing) para resolver Sudokus, con tres métodos de enfriamiento: geometric (g), slow (s) y linear (l).

## Estructura de `src/`
- `sudoku.py` : Código principal.  
- `run_all.py` : Ejecuta todos los ejemplares con cada método de enfriamiento.  
- `Ejemplares/` : Tableros de prueba (`David_Filmer1.txt`, `Easy1.txt`, `Hard1.txt`, `Medium1.txt`, `SD2.txt`).

## Requisitos
- Python 3.x  
- numpy

## Uso

### Resolver un Sudoku específico
```bash
cd src
python3 sudoku.py Ejemplares/Easy1.txt s

es decir, sigue la estructura de: `python sudoku.py archivo.txt metodo_enfriamiento`
