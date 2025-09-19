# Tarea 2 - Computo Evolutivo

## Ejecución
### Default
Se puede realizar la ejecución que ocupamos para nuestras pruebas simplemente escribiendo en la terminar 

```
python src/busqueda_local.py
```

En esta ejecución se muestran primero las soluciones iniciales (bits generados aleatoriamente) para cada una de las funciones, luego se muestran los valores reales de las soluciones y su valor (fitness) al ser evaluadas.

Las soluciones despues se someten al algoritmo de busqueda local, con las 3 tecnicas: mejor descenso, descenso aleatorio y primer descenso, reportando la mejor solución encontrada para cada método.

En esta ejecución las soluciones son de dimensión 10, codificadas con 10 bits de precisión y con un máximo de 50 épocas para cada método de busqueda. 

### Personalizada
Se incluye además una forma de ejecutar el programa eligiendo la función objetivo, la dimensión, cantidad de bits y el número de épocas, para lo que se leen los atributos correspondientes desde la linea de comandos:

```
python src/busqueda_local n d b i
```

donde:
- n es la función objetivo
- d la dimensión
- b número de bits para la representación
- i número máximo de épocas

Ejemplos de uso:
```
python src/busqueda_local.py                    # Ejecución por defecto
python src/busqueda_local.py 1 2 16 1000        # Sphere, 2D, 16 bits, 1000 iter
python src/busqueda_local.py 4 10 20 5000       # Rastrigin, 10D, 20 bits, 5000 iter
```

