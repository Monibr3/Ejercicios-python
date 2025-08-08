# Simulador de Cajero Automático - Nivel Intermedio
# --------------------------------------------------
# Este programa simula el funcionamiento básico de un cajero automático.
# El usuario debe ingresar un PIN para acceder a su cuenta. Tiene hasta 3 intentos.
# Una vez autenticado, puede realizar las siguientes operaciones:
#   1. Consultar saldo
#   2. Retirar dinero (si hay suficiente saldo)
#   3. Ingresar dinero
#   4. Salir
#
# El programa gestiona múltiples cuentas (simuladas mediante un diccionario),
# cada una identificada por su PIN como clave, y con un valor asociado que es otro
# diccionario con un solo dato: el "saldo".
#
# Además, incluye control de errores para evitar que el programa se bloquee si el
# usuario introduce datos no válidos (por ejemplo, letras en lugar de números al
# ingresar o retirar dinero).

# Diccionario que contiene las cuentas disponibles en el cajero.
# Clave: PIN (string)
# Valor: Diccionario con el saldo asociado a ese PIN

import getpass

cuentas = {
    "1234": {"saldo": 1000},
    "5678": {"saldo": 250},
    "4321": {"saldo": 10000},
    "9955": {"saldo": 5000}
}

# Inicializa el contador de intentos de ingreso de PIN
intentos = 0

# Variable que almacenará el PIN introducido por el usuario
pin_ingresado = ""

# Bucle que permite hasta 3 intentos para ingresar un PIN correcto
while intentos < 3:
    pin_ingresado =  getpass.getpass("Hola, introduzca su PIN\n")
    
    # Verifica si el PIN ingresado corresponde a una cuenta existente
    if pin_ingresado in cuentas:
        print("Acceso concedido\n")

        # Bucle principal del menú de operaciones del cajero
        while True:
            # Muestra las opciones disponibles al usuario
            print("¿Que operación quiere realizar?")
            print("1.-Consultar saldo")
            print("2.-Retirar dinero")
            print("3.-Ingresar dinero")
            print("4.-Salir")

            # El usuario elige una opción del menú
            opcion = input("Seleccione una opción (1-4): \n").strip()

            # Opción 1: Mostrar el saldo actual del usuario
            if opcion == "1":
                print(f'Su saldo actual es de {cuentas[pin_ingresado]["saldo"]} euros \n')

            # Opción 2: Retirar dinero del saldo
            elif opcion == "2":
                try:
                    # Solicita la cantidad a retirar e intenta convertirla en entero
                    retirar = int(input("¿Que cantidad desea retirar?\n"))
                    saldo = cuentas[pin_ingresado]["saldo"]

                    # Verifica si el saldo es suficiente para la retirada
                    if saldo < retirar:
                        print("No tiene saldo suficiente\n")
                    else:
                        # Actualiza el saldo restando la cantidad retirada
                        nuevo_saldo = saldo - retirar
                        cuentas[pin_ingresado]["saldo"] = nuevo_saldo
                        print(f"\nSu nuevo saldo es {cuentas[pin_ingresado]['saldo']} euros\n")
                except ValueError:
                    # Captura errores si el usuario no introduce un número válido
                    print("Error: ingrese una cantidad válida\n")

            # Opción 3: Ingresar dinero en la cuenta
            elif opcion == "3":
                try:
                    # Solicita la cantidad a ingresar e intenta convertirla en entero
                    ingresar = int(input("¿Que cantidad desea ingresar?\n"))
                    # Actualiza el saldo sumando la cantidad ingresada
                    nuevo_saldo = cuentas[pin_ingresado]["saldo"] + ingresar
                    cuentas[pin_ingresado]["saldo"] = nuevo_saldo
                    print(f"\nSu nuevo saldo es {cuentas[pin_ingresado]['saldo']} euros\n")
                except ValueError:
                    # Captura errores si el usuario no introduce un número válido
                    print("Error: ingrese una cantidad válida\n")

            # Opción 4: Salir del cajero
            elif opcion == "4":
                print("Gracias por usar nuestro cajero. ¡Hasta pronto!\n")
                break

            # En caso de que la opción introducida no sea válida
            else:
                print("Opción no válida. Intente de nuevo.\n")

        # Una vez dentro del sistema, si el usuario decide salir, se rompe el bucle exterior también
        break

    else:
        # Si el PIN no es válido, incrementa el contador de intentos
        print("PIN incorrecto, ingrese el PIN otra vez\n")
        intentos += 1

# Si se superan los 3 intentos sin ingresar un PIN válido, se deniega el acceso
if intentos == 3:
    print("PIN incorrecto más de 3 veces, entrada denegada\n")