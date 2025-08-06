# Programa que pregunta al usuario que operación desea realizar, 
# y despues le pide que introduzca los valores de las matrices


from itertools import chain


def sumar_matrices (matriz1,matriz2):
    """
    Suma dos matrices del mismo tamaño.

    Args:
        matriz1 : Primera matriz.
        matriz2 : Segunda matriz.

    Returns:
        Matriz resultado de la suma.
    """
    matriz_suma = []  # Inicializamos la matriz resultado

    for i in range(len(matriz1)):  # Recorremos las filas
        fila = [] # Creamos una nueva fila vacía
        for j in range(len(matriz1[0])):  # Recorre las columnas (j = índice de columna)
            fila.append(matriz1[i][j] + matriz2[i][j]) # Suma los valores en la misma posición
        matriz_suma.append(fila) # Añadimos la fila ya sumada a la matriz resultante

    return matriz_suma
def restar_matrices (matriz1,matriz2):
    """
    Resta  dos matrices del mismo tamaño.

    Args:
        matriz1 : Primera matriz.
        matriz2 : Segunda matriz.

    Returns:
        Matriz resultado de la resta.
    """
    matriz_resta = []  # Inicializamos la matriz resultado

    for i in range(len(matriz1)):  # Recorremos las filas
        fila = [] # Creamos una nueva fila vacía
        for j in range(len(matriz1[0])):  # Recorre las columnas (j = índice de columna)
            fila.append(matriz1[i][j] - matriz2[i][j]) # Resta los valores en la misma posición
        matriz_resta.append(fila) # Añadimos la fila ya restada a la matriz resultante

    return matriz_resta

def multiplicar_matrices (matriz1,matriz2):
    """
    Multiplica dos matrices si sus dimensiones son compatibles.

    Args:
        matriz1 : Primera matriz (m x n).
        matriz2 : Segunda matriz (n x p).

    Returns:
        Matriz resultante de tamaño (m x p), 
        donde cada elemento es el resultado de multiplicar filas de matriz1
        por columnas de matriz2.
 
        
    """

    # Validamos si las dimensiones permiten la multiplicación
    if len(matriz1[0]) != len(matriz2):
        raise ValueError("Las matrices no se pueden multiplicar: columnas de matriz1 ≠ filas de matriz2")

    matriz_multiplicacion = []  # Inicializamos la matriz resultado

    # Recorremos las filas de la primera matriz
    for i in range(len(matriz1)):
        fila = []  # Creamos una nueva fila para la matriz resultado

        # Recorremos las columnas de la segunda matriz
        for j in range(len(matriz2[0])):
            elemento = 0  # Acumulador para el valor de la posición [i][j]

            # Realizamos la multiplicación de la fila i por la columna j
            for k in range(len(matriz1[0])):
                elemento += matriz1[i][k] * matriz2[k][j]

            fila.append(elemento)  # Añadimos el valor calculado a la fila

        matriz_multiplicacion.append(fila)  # Añadimos la fila completa a la matriz resultado

    return matriz_multiplicacion

def obtener_menor(matriz, fila_a_eliminar,columna_a_eliminar):
    """
    Obtiene la submatriz menor eliminando la primera fila y la columna especificada.

    Args:
        matriz : Matriz original cuadrada.
        columna_a_eliminar : Índice de la columna que se eliminará.

    Returns:
        Submatriz resultante de eliminar la primera fila
        y la columna especificada de la matriz original.
    """
    submatriz = [] # Aquí almacenaremos la nueva submatriz (el menor)

     # Recorremos todas las filas con su índice
    for i,fila in enumerate(matriz):  
        if i == fila_a_eliminar:
            continue#saltamos la fina a eliminar
        nueva_fila = [] # Fila parcial que formará parte del menor
        # Recorremos cada valor de la fila con su índice de columna
        for j,valor in enumerate(fila):
            if j != columna_a_eliminar:   # Solo incluimos columnas que no eliminamos
                nueva_fila.append(valor) # Añadimos el valor a la fila filtrada
        submatriz.append(nueva_fila)  # Añadimos la fila a la submatriz
    return submatriz # Devolvemos el menor resultante

def determinante(matriz):
    """
    Calcula el determinante de una matriz cuadrada de cualquier tamaño usando recursión.

    Args:
        matriz : Matriz cuadrada de tamaño n x n.

    Returns:
         Valor del determinante de la matriz.

   
    """
    n = len(matriz[0])
    if n == 1:
        return matriz[0][0]  # Caso base: matriz 1x1
    elif n == 2:
        # Caso base: matriz 2x2 con fórmula directa
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]
    else:
        det = 0
        for j in range(n):
            # Calculamos el menor de la matriz para la columna j
            menor = obtener_menor(matriz,0, j)
            # Cofactor con signo alternado, elemento de la primera fila y determinante del menor
            cofactor = (-1) ** j * matriz[0][j] * determinante(menor)
            det += cofactor  # Sumamos el cofactor al determinante total
        return det

def matriz_traspuesta (matriz):
    """
    Calcula la matriz traspuesta de una matriz dada.

    Args:
        matriz: Matriz original de tamaño m x n.

    Returns:
        Matriz traspuesta de tamaño n x m,
        donde las filas y columnas están intercambiadas respecto a la matriz original.
    """
    filas = len (matriz)
    columnas = len(matriz[0])
    resultado = []
    for j in range (columnas):# Recorremos columnas
        fila = []
        for i in range(filas): # Recorremos filas
            fila.append(matriz[i][j])
        resultado.append(fila)
    return resultado

def matriz_cofactores(matriz):
    """
        Calcula la matriz de cofactores de una matriz cuadrada.

        Args:
            matriz : Matriz cuadrada original.

        Returns:
             Matriz de cofactores.
        """
    n = len(matriz)
    cofactores = []
    for i in range(n):
        fila_cofactores = []
        for j in range(n):
            menor = obtener_menor(matriz, i, j)  # Obtenemos el menor M_ij
            cofactor = (-1) ** (i + j) * determinante(menor)  # Aplicamos el signo y determinante
            fila_cofactores.append(cofactor)
        cofactores.append(fila_cofactores)
    return cofactores

def matriz_inversa(matriz):
    """
    Calcula la matriz inversa de una matriz cuadrada (si existe).

    Args:
        matriz : Lista de listas que representa una matriz cuadrada.

    Returns:
        Lista de listas que representa la matriz inversa.

    Raises:
        ValueError: Si la matriz no es cuadrada o su determinante es cero.
    """

    filas = len(matriz)             # Número de filas
    columnas = len(matriz[0])       # Número de columnas

    # Paso 1: Verificamos que sea cuadrada
    if filas != columnas:
        raise ValueError("La matriz debe ser cuadrada para poder calcular su inversa.")

    # Paso 2: Calculamos el determinante
    det = determinante(matriz)

    if det == 0:
        # Si el determinante es 0, la matriz no tiene inversa
        raise ValueError("La matriz no tiene inversa porque su determinante es cero.")

    # Paso 3: Calculamos la matriz de cofactores
    cofactores = matriz_cofactores(matriz)

    # Paso 4: Transponemos la matriz de cofactores para obtener la adjunta
    adjunta = matriz_traspuesta(cofactores)

    # Paso 5: Dividimos cada elemento de la adjunta entre el determinante
    inversa = []
    for fila in adjunta:
        fila_inversa = []
        for elemento in fila:
            fila_inversa.append(elemento / det)  # División escalar
        inversa.append(fila_inversa)

    return inversa


def leer_matriz(nombre, filas, columnas):
    """
    Crea una matriz con los datos del usuario.

    Args:
        matriz: Matriz a crear, numero de filas y de columnas.

    Returns:
        Matriz creada.
    """
    print(f"Introduce los valores de la matriz {nombre}:")
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = int(input(f'Valor [{i}][{j}]: '))
            fila.append(valor)
        matriz.append(fila)
    return matriz


def imprimir_matriz(matriz):#Saca por pantalla la matriz resultado
    for fila in matriz:
        print(fila)

def introducir_matrices_misma_dimension(nombre1, nombre2):
    n = int(input("Número de filas: "))
    m = int(input("Número de columnas: "))
    matriz1 = leer_matriz(nombre1, n, m)
    matriz2 = leer_matriz(nombre2, n, m)
    return matriz1, matriz2

# Ahora desarollamos la parte principal del programa
def main():
    opcion = 0
    while opcion!= 7: # Mientras no se elija la opción de salir, se sigue ejecutando el bucle
        print("\n---MENÚ DE OPERACIONES---")
        print("1.-sumar Matrices")
        print("2.-Restar Matrices")
        print("3.-Multiplicar Matrices")
        print("4.-Matriz Transpuesta")
        print("5.-Determinante de una Matriz")
        print("6.-Matriz Inversa")
        print("7.-Salir")
        try:
            opcion = int(input("Elige una opción (1-7): "))
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número del 1 al 7.")
            continue
        if opcion < 1 or opcion > 7:
            print("Opción incorrecta. Inténtalo de nuevo.")
        elif opcion == 1:
            
                try:
                # Obtenemos las matrices
                    matriz1 , matriz2 = introducir_matrices_misma_dimension("1","2")

                except ValueError:
                    print("Entrada inválida. Por favor, introduce números enteros.\n")

                # Sumamos las matrices
                suma = sumar_matrices(matriz1, matriz2)

                # Mostramos el resultado
                imprimir_matriz(suma)

        elif opcion == 2:
            
                try:
                    # Obtenemos las matrices
                    matriz1 , matriz2 = introducir_matrices_misma_dimension("1","2")

                except ValueError:
                    print("Entrada inválida. Por favor, introduce números enteros.\n")


                # Restamos las matrices
                resta = restar_matrices(matriz1, matriz2)

                # Mostramos el resultado
                imprimir_matriz(resta)

        elif opcion == 3:
            
                try:
                    # Pedimos dimensiones las matrices asegurandonos que tienen las dimensiones adecuadas)
                    n = int(input("Introduce el número de columnas de la primera matriz y el número de filas de la segunda: "))
                    m = int(input("Introduce el número de filas de la primera matriz:"))
                    t = int(input("Introduce el número de columnas de la segunda matriz:"))
                    # Inicializamos las matrices vacías
                    matriz1 = leer_matriz("1",m,n)
                    matriz2 = leer_matriz("2",n,t)

                except ValueError:
                    print("Entrada inválida. Por favor, introduce números enteros.\n")


                # Multiplicamos las matrices
                multiplicacion = multiplicar_matrices(matriz1, matriz2)

                # Mostramos el resultado
                imprimir_matriz(multiplicacion)

        elif opcion == 4:
            
                try:
                    # Pedimos dimensiones la matriz
                    n = int(input("Introduce el número de filas de la  matriz : "))
                    m = int(input("Introduce el número de columnas de la matriz:"))
                    
                    # Inicializamos la matriz vacia
                    matriz1 = leer_matriz("1",n,m)
                    

                except ValueError:
                    print("Entrada inválida. Por favor, introduce números enteros.\n")


                # Calculamos su determinante
                trans= matriz_traspuesta(matriz1)

                # Mostramos el resultado
                imprimir_matriz(trans)


        elif opcion == 5:
            
                try:
                    # Pedimos dimensiones la matriz
                    n = int(input("Introduce el número de filas y columas de la  matriz(matriz cuadrada) : "))
                                    
                    # Inicializamos la matriz vacia
                    matriz1 = leer_matriz("1",n,n)
                    

                except ValueError:
                    print("Entrada inválida. Por favor, introduce números enteros.\n")


                # Calculamos su determinante
                det= determinante(matriz1)

                # Mostramos el resultado
                print(f"El determinante de la matriz es: {det}")
                

        elif opcion == 6:
            
                try:
                    # Pedimos dimensiones la matriz
                    n = int(input("Introduce el número de filas y columnas de la  matriz (matriz cuadrda): "))
                                
                    # Inicializamos la matriz vacia
                    matriz1 = leer_matriz("1",n,n)
                    

                except ValueError:
                    print("Entrada inválida. Por favor, introduce números enteros.\n")


                # Calculamos la matriz inversa
                inversa= matriz_inversa(matriz1)

                # Mostramos el resultado
                imprimir_matriz(inversa)


if __name__ == "__main__":
    main()















