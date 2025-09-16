import numpy as np
import random
from codificacion import decodifica_array
from EvaluacionFunciones import sphere, ackley, griewank, rastrigin, rosenbrock

class BusquedaLocal:
    def __init__(self, funcion_objetivo, dimension, bits_por_var, rango_min, rango_max):

        self.funcion_objetivo = funcion_objetivo
        self.dimension = dimension
        self.bits_por_var = bits_por_var
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.total_bits = dimension * bits_por_var
    
    def generar_solucion_aleatoria(self):
        return np.random.randint(0, 2, size=(self.dimension, self.bits_por_var))
    
    def generar_vecindad(self, solucion):
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
        valores_reales = []
        
        for i in range(self.dimension):
            bits_variable = matriz_bits[i, :].tolist() 
            from codificacion import decodifica
            valor_real = decodifica(bits_variable, self.bits_por_var, 
                                  self.rango_min, self.rango_max)
            valores_reales.append(valor_real)
        
        x = np.array(valores_reales)
        return self.funcion_objetivo(x)
    
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
            
            for vecino in vecinos:
                fitness_vecino = self.evaluar_solucion(vecino)
                evaluaciones += 1
                
                if fitness_vecino < mejor_fitness:  
                    mejor_vecino = vecino
                    mejor_fitness = fitness_vecino
            
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
            random.shuffle(vecinos) 
            
            mejor_vecino = None
            mejor_fitness = fitness_actual
            
            for vecino in vecinos:
                fitness_vecino = self.evaluar_solucion(vecino)
                evaluaciones += 1
                
                if fitness_vecino < fitness_actual: 
                    mejor_vecino = vecino
                    mejor_fitness = fitness_vecino
                    break  
            
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
            
            for vecino in vecinos:
                fitness_vecino = self.evaluar_solucion(vecino)
                evaluaciones += 1
                
                if fitness_vecino < fitness_actual: 
                    mejor_vecino = vecino
                    mejor_fitness = fitness_vecino
                    break  
            
            if mejor_vecino is None:
                break
                
            solucion_actual = mejor_vecino
            fitness_actual = mejor_fitness
        
        return solucion_actual, fitness_actual, evaluaciones

if __name__ == "__main__":
    
    dimension = 10
    bits_por_var = 10  
    bl = BusquedaLocal(sphere, dimension, bits_por_var, -5.12, 5.12)
    b2 = BusquedaLocal(ackley, dimension, bits_por_var, -30, 30)
    b3 = BusquedaLocal(griewank, dimension, bits_por_var, -600, 600)
    b4 = BusquedaLocal(rastrigin, dimension, bits_por_var, -5.12, 5.12)
    b5 = BusquedaLocal(rosenbrock, dimension, bits_por_var, -2.048, 2.048)



    print(f"Config: dim={dimension}, bits={bits_por_var}")
    
  
    esfera = bl.generar_solucion_aleatoria()
    akli = b2.generar_solucion_aleatoria()
    grigan = b3.generar_solucion_aleatoria()
    rastrin = b4.generar_solucion_aleatoria()
    rosenbok = b5.generar_solucion_aleatoria()
    ##########################################################################
    
    print(f"Matriz de bits Sphere:\n{esfera}")
    v1 = bl.mostrar_solucion(esfera)
    print(f"Matriz de bits ackley :\n{akli}")
    v2 = b2.mostrar_solucion(akli)
    print(f"Matriz de bits griewank :\n{grigan}")
    v3 = b3.mostrar_solucion(grigan)
    print(f"Matriz de bits rastrigin :\n{rastrin}")
    v4 = b4.mostrar_solucion(rastrin)
    print(f"Matriz de bits rosenbrock :\n{rosenbok}")
    v5 = b5.mostrar_solucion(rosenbok)



    print(f"Valores reales Sphere : {[round(x, 3) for x in v1]}")
    fitness = bl.evaluar_solucion(esfera)
    print(f"Fitness: {fitness:.6f}")


    print(f"Valores reales ackley: {[round(x, 3) for x in v2]}")
    f1 = b2.evaluar_solucion(akli)
    print(f"Fitness: {f1:.6f}")


    print(f"Valores reales griewank: {[round(x, 3) for x in v3]}")
    f2 = b3.evaluar_solucion(grigan)
    print(f"Fitness: {f2:.6f}")


    print(f"Valores reales rastrigin: {[round(x, 3) for x in v4]}")
    f3 = b4.evaluar_solucion(rastrin)
    print(f"Fitness: {f3:.6f}")

    print(f"Valores reales rosenbrock: {[round(x, 3) for x in v5]}")
    f4 = b5.evaluar_solucion(rosenbok)
    print(f"Fitness: {f4:.6f}")
    
    # Probar las 3 variantes
    algoritmos = [
        ("Mayor Descenso Esfera", bl.mayor_descenso),
        ("Descenso Aleatorio Esfera", bl.descenso_aleatorio), 
        ("Primer Descenso Esfera", bl.primer_descenso)
    ]
    
    for nombre, algoritmo in algoritmos:
        print(f"\n {nombre}:")
        solucion, fitness, evals = algoritmo(max_iter=50)
        r1 = bl.mostrar_solucion(solucion)
        print(f"   Valores: {[round(x, 3) for x in r1]}")
        print(f"   f(x) = {fitness:.6f}, Evaluaciones: {evals}")

    algoritmos2 = [
        ("Mayor Descenso ackley", b2.mayor_descenso),
        ("Descenso Aleatorio ackley", b2.descenso_aleatorio), 
        ("Primer Descenso ackley", b2.primer_descenso)
    ]

    for nombre, algoritmo in algoritmos2:
        print(f"\n {nombre}:")
        solucion, f1, evals = algoritmo(max_iter=50)
        r2 = b2.mostrar_solucion(solucion)
        print(f"   Valores: {[round(x, 3) for x in r2]}")
        print(f"   f(x) = {f2:.6f}, Evaluaciones: {evals}")

    algoritmos3 = [
        ("Mayor Descenso griewank", b3.mayor_descenso),
        ("Descenso Aleatorio griewank", b3.descenso_aleatorio), 
        ("Primer Descenso griewank", b3.primer_descenso)
    ]
    
    for nombre, algoritmo in algoritmos3:
        print(f"\n {nombre}:")
        solucion, f2, evals = algoritmo(max_iter=50) 
        r3 = b3.mostrar_solucion(solucion)
        print(f"   Valores: {[round(x, 3) for x in r3]}")
        print(f"   f(x) = {f2:.6f}, Evaluaciones: {evals}")

    algoritmos4 = [
        ("Mayor Descenso rastrigin", b4.mayor_descenso),
        ("Descenso Aleatorio rastrigin", b4.descenso_aleatorio), 
        ("Primer Descenso rastrigin", b4.primer_descenso)
    ]
    
    for nombre, algoritmo in algoritmos4:
        print(f"\n {nombre}:")
        solucion, f3, evals = algoritmo(max_iter=50) 
        r4 = b4.mostrar_solucion(solucion)
        print(f"   Valores: {[round(x, 3) for x in r4]}")
        print(f"   f(x) = {f3:.6f}, Evaluaciones: {evals}")

    algoritmos5 = [
        ("Mayor Descenso rosenbrock", b5.mayor_descenso),
        ("Descenso Aleatorio rosenbrock", b5.descenso_aleatorio), 
        ("Primer Descenso rosenbrock", b5.primer_descenso)
    ]
    
    for nombre, algoritmo in algoritmos5:
        print(f"\n {nombre}:")
        solucion, f4, evals = algoritmo(max_iter=50)
        r5 = b5.mostrar_solucion(solucion)
        print(f"   Valores: {[round(x, 3) for x in r5]}")
        print(f"   f(x) = {f4:.6f}, Evaluaciones: {evals}")

    print(f"\n Todos los ejemplos han funcionado!")