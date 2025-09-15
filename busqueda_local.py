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
        Genera una solución aleatoria como matriz de bits.
        
        Returns:
            Matriz numpy de forma (dimension, bits_por_var) con 0s y 1s
        """
        return np.random.randint(0, 2, size=(self.dimension, self.bits_por_var))
    
    def generar_vecindad(self, solucion):
        """
        Genera todos los vecinos de una solución mediante flip de 1 bit.
        Vecindad de Hamming distance = 1.
        
        Args:
            solucion: Matriz de bits de forma (dimension, bits_por_var)
            
        Returns:
            Lista de matrices vecinas (cada una con 1 bit diferente)
        """
        vecinos = []
        filas, cols = solucion.shape
        
        for i in range(filas):
            for j in range(cols):
                # Crear vecino flippeando el bit (i,j)
                vecino = solucion.copy()
                vecino[i, j] = 1 - vecino[i, j]  # Flip: 0->1, 1->0
                vecinos.append(vecino)
        return vecinos
    
    def evaluar_solucion(self, matriz_bits):
        """
        Evalúa una solución (matriz de bits) decodificándola y aplicando la función objetivo.
        
        Args:
            matriz_bits: Matriz de bits de forma (dimension, bits_por_var)
            
        Returns:
            Valor de la función objetivo
        """
        valores_reales = []
        
        # Decodificar cada fila (variable) de la matriz
        for i in range(self.dimension):
            bits_variable = matriz_bits[i, :].tolist()  # Convertir fila a lista
            # Usar la función de decodificación existente
            from codificacion import decodifica
            valor_real = decodifica(bits_variable, self.bits_por_var, 
                                  self.rango_min, self.rango_max)
            valores_reales.append(valor_real)
        
        # Convertir a numpy array y evaluar
        x = np.array(valores_reales)
        return self.funcion_objetivo(x)
    
    def matriz_a_vector(self, matriz_bits):
        """Convierte matriz de bits a vector lineal para compatibilidad."""
        return matriz_bits.flatten()
    
    def vector_a_matriz(self, vector_bits):
        """Convierte vector lineal a matriz de bits."""
        return np.array(vector_bits).reshape(self.dimension, self.bits_por_var)
    
    def mostrar_solucion(self, matriz_bits):
        """Muestra la solución de forma legible."""
        valores_reales = []
        for i in range(self.dimension):
            bits_variable = matriz_bits[i, :].tolist()
            from codificacion import decodifica
            valor_real = decodifica(bits_variable, self.bits_por_var, 
                                  self.rango_min, self.rango_max)
            valores_reales.append(valor_real)
        return valores_reales
    
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
    print("🔍 BÚSQUEDA LOCAL (Matriz)")
    print("=" * 40)
    
    # Configuración
    dimension = 2
    bits_por_var = 4  # Menos bits para visualizar mejor
    bl = BusquedaLocal(sphere, dimension, bits_por_var, -5.12, 5.12)
    
    print(f"Config: dim={dimension}, bits={bits_por_var}")
    
    # Mostrar ejemplo de solución como matriz
    print(f"\n Ejemplo de solución aleatoria:")
    solucion_ejemplo = bl.generar_solucion_aleatoria()
    print(f"Matriz de bits:\n{solucion_ejemplo}")
    valores = bl.mostrar_solucion(solucion_ejemplo)
    print(f"Valores reales: {[round(x, 3) for x in valores]}")
    fitness = bl.evaluar_solucion(solucion_ejemplo)
    print(f"Fitness: {fitness:.6f}")
    
    # Probar las 3 variantes
    algoritmos = [
        ("Mayor Descenso", bl.mayor_descenso),
        ("Descenso Aleatorio", bl.descenso_aleatorio), 
        ("Primer Descenso", bl.primer_descenso)
    ]
    
    for nombre, algoritmo in algoritmos:
        print(f"\n {nombre}:")
        solucion, fitness, evals = algoritmo(max_iter=50)
        valores = bl.mostrar_solucion(solucion)
        print(f"   Valores: {[round(x, 3) for x in valores]}")
        print(f"   f(x) = {fitness:.6f}, Evaluaciones: {evals}")

    print(f"\n Todos los ejemplos han funcionado!")