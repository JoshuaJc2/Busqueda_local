def codifica(x, n_bits, a, b):
    """
    Codifica un valor real x en una representación binaria de n_bits bits.
    
    Args:
        x: Valor real a codificar
        n_bits: Número de bits para la representación
        a: Límite inferior del rango
        b: Límite superior del rango
    
    Returns:
        Lista de enteros (0 o 1) representando la codificación binaria
    """
    max_val = (1 << n_bits) - 1  # 2^n_bits - 1
    k = round((x - a) * max_val / (b - a))
    bits = [0] * n_bits
    
    for i in range(n_bits - 1, -1, -1):
        bits[i] = k % 2
        k //= 2
    
    return bits


def decodifica(x_cod, n_bits, a, b):
    """
    Decodifica una representación binaria a un valor real.
    
    Args:
        x_cod: Lista de bits (0s y 1s)
        n_bits: Número de bits
        a: Límite inferior del rango
        b: Límite superior del rango
    
    Returns:
        Valor real decodificado
    """
    k = 0
    for i in range(n_bits):
        k = (k << 1) | x_cod[i]
    
    max_val = (1 << n_bits) - 1
    return a + k * (b - a) / max_val


def codifica_array(x, dim_x, n_bits, a, b):
    """
    Codifica un array de valores reales.
    
    Args:
        x: Array de valores reales a codificar
        dim_x: Dimensión del array (número de elementos)
        n_bits: Número de bits por elemento
        a: Límite inferior del rango
        b: Límite superior del rango
    
    Returns:
        Lista de bits concatenados de todas las codificaciones
    """
    res = [0] * (dim_x * n_bits)
    for i in range(dim_x):
        bits = codifica(x[i], n_bits, a, b)
        for j in range(n_bits):
            res[i * n_bits + j] = bits[j]
    
    return res


def decodifica_array(x_cod, dim_x, n_bits, a, b):
    """
    Decodifica un array de bits a valores reales.
    
    Args:
        x_cod: Array de bits codificados
        dim_x: Número de elementos a decodificar
        n_bits: Número de bits por elemento
        a: Límite inferior del rango
        b: Límite superior del rango
    
    Returns:
        Lista de valores reales decodificados
    """
    res = [0.0] * dim_x
    for i in range(dim_x):
        bits = [0] * n_bits
        for j in range(n_bits):
            bits[j] = x_cod[i * n_bits + j]
        res[i] = decodifica(bits, n_bits, a, b)
    
    return res


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo con un solo valor
    valor = 3.5
    n_bits = 8
    a = 0.0
    b = 10.0
    
    print(f"Valor original: {valor}")
    
    # Codificar
    bits_codificados = codifica(valor, n_bits, a, b)
    print(f"Bits codificados: {bits_codificados}")
    
    # Decodificar
    valor_decodificado = decodifica(bits_codificados, n_bits, a, b)
    print(f"Valor decodificado: {valor_decodificado}")
    
    print("\n" + "="*50 + "\n")
    
    # Ejemplo con array
    valores = [1.2, 5.7, 8.3]
    dim_x = len(valores)
    
    print(f"Valores originales: {valores}")
    
    # Codificar array
    bits_array = codifica_array(valores, dim_x, n_bits, a, b)
    print(f"Bits del array: {bits_array}")
    
    # Decodificar array
    valores_decodificados = decodifica_array(bits_array, dim_x, n_bits, a, b)
    print(f"Valores decodificados: {valores_decodificados}")