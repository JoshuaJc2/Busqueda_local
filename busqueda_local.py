import numpy as np
import random
from codificacion import decodifica_array
from EvaluacionFunciones import sphere, ackley, griewank, rastrigin, rosenbrock

class BusquedaLocal:
    def __init__(self, funcion_objetivo, dimension, bits_por_var, rango_min, rango_max):
        """
        Inicializa la búsqueda local.
        
        Args:
            funcion_objetivo: Función a optimizar (sphere, ackley, etc.)
            dimension: Número de variables
            bits_por_var: Bits por variable
            rango_min: Límite inferior del rango
            rango_max: Límite superior del rango
        """
        self.funcion_objetivo = funcion_objetivo
        self.dimension = dimension
        self.bits_por_var = bits_por_var
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.total_bits = dimension * bits_por_var
    
    def generar_solucion_aleatoria(self):
        """
        Genera una solución aleatoria como vector de bits.
        
        Returns:
            Lista de bits (0s y 1s) de tamaño dimension * bits_por_var
        """
        return [random.randint(0, 1) for _ in range(self.total_bits)]
    
    def generar_vecindad(self, solucion):
        """
        Genera todos los vecinos de una solución mediante flip de 1 bit.
        Vecindad de Hamming distance = 1.
        
        Args:
            solucion: Vector de bits actual
            
        Returns:
            Lista de vectores vecinos (cada uno con 1 bit diferente)
        """
        vecinos = []
        for i in range(len(solucion)):
            # Crear vecino flippeando el bit i
            vecino = solucion.copy()
            vecino[i] = 1 - vecino[i]  # Flip: 0->1, 1->0
            vecinos.append(vecino)
        return vecinos
    
    def evaluar_solucion(self, bits):
        """
        Evalúa una solución (vector de bits) decodificándola y aplicando la función objetivo.
        
        Args:
            bits: Vector de bits
            
        Returns:
            Valor de la función objetivo
        """
        # Decodificar bits a valores reales
        valores_reales = decodifica_array(bits, self.dimension, self.bits_por_var, 
                                        self.rango_min, self.rango_max)
        
        # Convertir a numpy array y evaluar
        x = np.array(valores_reales)
        return self.funcion_objetivo(x)

# Ejemplo de uso y pruebas
if __name__ == "__main__":
    print("🔍 BÚSQUEDA LOCAL - Generador y Vecindad")
    print("=" * 50)
    
    # Configuración
    dimension = 2
    bits_por_var = 8
    rango_min = -5.12
    rango_max = 5.12
    
    # Crear instancia para función Sphere
    bl = BusquedaLocal(sphere, dimension, bits_por_var, rango_min, rango_max)
    
    print(f"Dimensión: {dimension}")
    print(f"Bits por variable: {bits_por_var}")
    print(f"Total de bits: {bl.total_bits}")
    print(f"Rango: [{rango_min}, {rango_max}]")
    
    # Generar solución aleatoria
    print("\n📍 Generando solución aleatoria:")
    solucion = bl.generar_solucion_aleatoria()
    print(f"Bits: {solucion}")
    
    # Evaluar solución
    fitness = bl.evaluar_solucion(solucion)
    print(f"Fitness: {fitness:.6f}")
    
    # Generar vecindad
    print(f"\n🏘️  Generando vecindad (primeros 5 vecinos):")
    vecinos = bl.generar_vecindad(solucion)
    print(f"Total de vecinos: {len(vecinos)}")
    
    for i in range(min(5, len(vecinos))):
        vecino = vecinos[i]
        fitness_vecino = bl.evaluar_solucion(vecino)
        # Mostrar qué bit cambió
        diff_pos = [j for j in range(len(solucion)) if solucion[j] != vecino[j]][0]
        print(f"Vecino {i+1} (bit {diff_pos}): fitness = {fitness_vecino:.6f}")
    
    print(f"\n✅ Generador y operador de vecindad funcionando correctamente!")