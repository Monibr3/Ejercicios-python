# Programa que genera un número aleatorio entre 1 y 100 y el usuario ha de adivinarlo
# Incluye control de errores y cuenta los intentos

import random # Importamos el módulo random para generar números aleatorios

#generamos el número aleatorio
numero = random.randint(1,100)

# Inicializamos el contador de intentos
intentos = 0  

# Mostramos un mensaje inicial al usuario
print("Adivina un número del 1 al 100")

# Iniciamos un bucle que se repetirá hasta que el usuario acierte
while True:
    # Solicitamos al usuario que introduzca un número
    entrada = input("Introduce tu número: ")
    
    # Intentamos convertir la entrada a entero
    try:
        
        num = int(entrada)  # Convertimos la entrada a entero
        intentos += 1       # Sumamos un intento

       
        if num < 1 or num > 100:
            print(" Por favor, introduce un número entre 1 y 100.")
            continue #si el numero está fuera de rango vuelve al inicio del bucle

        # Comparamos el número introducido con el número secreto
        if num < numero:
            print("El número que buscamos es mayor.")
        elif num > numero:
            print("El número que buscamos es menor.")
        else:
            # Si acierta, mostramos un mensaje de éxito y salimos del bucle
            print(f"¡Has acertado! El número era {numero}.")
            print(f"Lo lograste en {intentos} intentos.")
            break # Salimos del bucle
    
    except ValueError:
        # Si el usuario introduce algo que no es un número, mostramos un aviso
        print("Eso no es un número válido. Inténtalo de nuevo.")