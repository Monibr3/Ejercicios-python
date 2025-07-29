# Programa que muestra un menú por pantalla para seleccionar una opción
opcion = 0
while opcion!= 5: # Mientras no se elija la opción de salir, se sigue ejecutando el bucle
    print("\n---MENÚ DE OPERACIONES---")
    print("1.-sumar")
    print("2.-Restar")
    print("3.-Multiplicar")
    print("4.-Dividir")
    print("5.-Salir")
    try:
        opcion = int(input("Elige una opción (1-5): "))
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número del 1 al 5.")
        continue
    if opcion < 1 or opcion > 5:
        print("Opción incorrecta. Inténtalo de nuevo.")

    elif opcion == 1: # Suma
        try:
            suma = 0
            cantidad = int(input("¿cuantos números quieres sumar?: "))# Por si queremos sumar mas de dos números
            for i in range(cantidad):
                numero = float(input(f"Introduce el número {i + 1}: "))
                suma += numero
            print(f"la suma total es {suma}")
        except ValueError:
            print("Entrada inválida. Solo se permiten números.")
    elif opcion == 2:# Resta
        try:
            minuendo = float(input('introduce el minuendo: '))
            sustraendo = float(input('introduce el sustraendo: '))
            resta = minuendo - sustraendo
            print(f'El resultado de la resta es {resta}')
        except ValueError:
            print("Entrada inválida.")

    elif opcion == 3:#Multiplicación
        try:
            numero1 = float(input('Introduce el primer número:'))
            numero2 = float(input('Introduce el segundo número:'))
            multipli = numero1 * numero2
            print(f'El resultado de la multiplicación es {multipli}')
        except ValueError:
            print("Entrada inválida.")

    elif opcion == 4:#División
        try:
            dividendo = float(input('Introduce el dividendo: '))
            divisor = float(input('Introduce el divisor: '))
            if divisor == 0:
                print("No se puede dividir por cero.")
            else:
                resultado = dividendo / divisor
                print(f"El resultado de la división es {resultado}")
        except ValueError:
            print("Entrada inválida.")
print("Gracias por usar la calculadora")#ya se escogió la opción 5 sale del bucle con una despedida
