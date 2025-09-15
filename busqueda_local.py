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
    
    def mayor_descenso(self, max_iter=1000):
        """
        Búsqueda por descenso - Mayor descenso.
        Explora TODOS los vecinos y elige el mejor.
        """
        solucion_actual = self.generar_solucion_aleatoria()
        fitness_actual = self.evaluar_solucion(solucion_actual)
        evaluaciones = 1
        
        for iteracion in range(max_iter):
            vecinos = self.generar_vecindad(solucion_actual)
            mejor_vecino = None
            mejor_fitness = fitness_actual
            
            # Evaluar todos los vecinos
            for vecino in vecinos:
                fitness_vecino = self.evaluar_solucion(vecino)
                evaluaciones += 1
                
                if fitness_vecino < mejor_fitness:  # Minimización
                    mejor_vecino = vecino
                    mejor_fitness = fitness_vecino
            
            # Si no hay mejora, terminar
            if mejor_vecino is None:
                break
                
            solucion_actual = mejor_vecino
            fitness_actual = mejor_fitness
        
        return solucion_actual, fitness_actual, evaluaciones
    
    def descenso_aleatorio(self, max_iter=1000):
        """
        Búsqueda por descenso - Descenso aleatorio.
        Explora vecinos aleatoriamente hasta encontrar mejora.
        """
        solucion_actual = self.generar_solucion_aleatoria()
        fitness_actual = self.evaluar_solucion(solucion_actual)
        evaluaciones = 1
        
        for iteracion in range(max_iter):
            vecinos = self.generar_vecindad(solucion_actual)
            random.shuffle(vecinos)  # Orden aleatorio
            
            mejor_vecino = None
            mejor_fitness = fitness_actual
            
            # Evaluar vecinos hasta encontrar mejora
            for vecino in vecinos:
                fitness_vecino = self.evaluar_solucion(vecino)
                evaluaciones += 1
                
                if fitness_vecino < fitness_actual:  # Minimización
                    mejor_vecino = vecino
                    mejor_fitness = fitness_vecino
                    break  # Tomar el primer mejor
            
            # Si no hay mejora, terminar
            if mejor_vecino is None:
                break
                
            solucion_actual = mejor_vecino
            fitness_actual = mejor_fitness
        
        return solucion_actual, fitness_actual, evaluaciones
    
    def primer_descenso(self, max_iter=1000):
        """
        Búsqueda por descenso - Primer descenso.
        Toma el PRIMER vecino que sea mejor.
        """
        solucion_actual = self.generar_solucion_aleatoria()
        fitness_actual = self.evaluar_solucion(solucion_actual)
        evaluaciones = 1
        
        for iteracion in range(max_iter):
            vecinos = self.generar_vecindad(solucion_actual)
            
            mejor_vecino = None
            mejor_fitness = fitness_actual
            
            # Tomar el primer vecino mejor
            for vecino in vecinos:
                fitness_vecino = self.evaluar_solucion(vecino)
                evaluaciones += 1
                
                if fitness_vecino < fitness_actual:  # Minimización
                    mejor_vecino = vecino
                    mejor_fitness = fitness_vecino
                    break  # Primer mejor encontrado
            
            # Si no hay mejora, terminar
            if mejor_vecino is None:
                break
                
            solucion_actual = mejor_vecino
            fitness_actual = mejor_fitness
        
        return solucion_actual, fitness_actual, evaluaciones

# Ejemplo de uso y pruebas
if __name__ == "__main__":
    print("🔍 BÚSQUEDA LOCAL")
    print("=" * 40)
    
    # Configuración
    dimension = 2
    bits_por_var = 8
    bl = BusquedaLocal(sphere, dimension, bits_por_var, -5.12, 5.12)
    
    print(f"Config: dim={dimension}, bits={bits_por_var}, total_bits={bl.total_bits}")
    
    # Probar las 3 variantes
    algoritmos = [
        ("Mayor Descenso", bl.mayor_descenso),
        ("Descenso Aleatorio", bl.descenso_aleatorio), 
        ("Primer Descenso", bl.primer_descenso)
    ]
    
    for nombre, algoritmo in algoritmos:
        print(f"\n🚀 {nombre}:")
        solucion, fitness, evals = algoritmo(max_iter=100)
        print(f"   Resultado: f(x) = {fitness:.6f}, Evaluaciones: {evals}")
    
    print(f"\n✅ Todos los algoritmos funcionando!")