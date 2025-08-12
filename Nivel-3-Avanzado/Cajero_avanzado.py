# Simulador de Cajero Automático - Nivel Intermedio-Alto
# ------------------------------------------------------
# Este programa simula el funcionamiento de un cajero automático realista,
# utilizando una base de datos para gestionar múltiples cuentas bancarias.
#
# El usuario debe autenticarse con su número de cuenta y un PIN, que se solicita
# de forma segura usando la librería 'getpass' para ocultar la entrada del PIN en pantalla.
# Se permiten hasta 3 intentos fallidos antes de denegar el acceso.
#
# Una vez autenticado, el usuario puede:
#   1. Consultar su saldo actual.
#   2. Retirar dinero, siempre que tenga saldo suficiente.
#   3. Ingresar dinero en su cuenta.
#   4. Salir del sistema.
#
# El programa actualiza en tiempo real los saldos en la base de datos para mantener
# la integridad y persistencia de los datos.
#
# Además, incluye manejo de errores para evitar que entradas inválidas (como letras
# en lugar de números) causen fallos inesperados en la ejecución.
#
# La gestión de cuentas, operaciones y conexión con la base de datos se realiza
# mediante una clase especializada, lo que facilita la escalabilidad y mantenimiento.

import getpass   # Módulo que permite introducir contraseñas sin que se muestren en pantalla.
import sqlite3   # Módulo para trabajar con bases de datos SQLite.
import Gestión_de_cuentas_bancarias as gb  # Importa el módulo con la lógica de cuentas y la clase BaseDatos.


# Creamos una instancia de la clase BaseDatos para acceder a las operaciones sobre la BD.
base_datos = gb.BaseDatos()

# Función auxiliar para guardar en la base de datos el saldo actualizado de la cuenta actual.
# Se llama después de ingresar o retirar dinero.
def guardar_cambios():
    base_datos.actualizar_saldo(cuenta.numero_cuenta, cuenta.saldo)


# Inicializa el contador de intentos fallidos de ingreso de PIN
intentos = 0

# Bucle que permite hasta 3 intentos para iniciar sesión correctamente
while intentos < 3:
    # Solicita el número de cuenta al usuario
    ncuenta_ingresado = input("Hola, introduzca su número de cuenta \n")
    # Solicita el PIN usando getpass para que no aparezca en pantalla mientras se escribe
    pin_ingresado = getpass.getpass("Hola, introduzca su PIN\n")
    
    # Verifica si la cuenta existe en la base de datos y obtiene un objeto Cuenta
    cuenta = base_datos.obtener_cuenta(ncuenta_ingresado) 
    
    # Comprueba que la cuenta exista y que el PIN sea correcto
    if cuenta and cuenta.verificar_pin(pin_ingresado):
        print("Acceso concedido")
        
        # Bucle principal del menú del cajero automático
        while True:
            print("¿Que operación quiere realizar?")
            print("1.-Consultar saldo")
            print("2.-Retirar dinero")
            print("3.-Ingresar dinero")
            print("4.-Salir")

            # El usuario elige una opción del menú
            opcion = input("Seleccione una opción (1-4): \n").strip()

            # Opción 1: Mostrar saldo actual
            if opcion == "1":
                print(f'Su saldo actual es de {cuenta.mostrar_saldo()} euros \n')

            # Opción 2: Retirar dinero
            elif opcion == "2":
                try:
                    saldo_retirar = int(input("¿Que cantidad desea retirar?\n"))
                    cuenta.retirar(saldo_retirar)  
                    guardar_cambios()  # Actualiza saldo en la base de datos
                except ValueError:
                    print("Error: ingrese una cantidad válida\n")

            # Opción 3: Ingresar dinero
            elif opcion == "3":
                try:
                    saldo_ingresar = int(input("¿Que cantidad desea ingresar?\n"))
                    cuenta.ingresar(saldo_ingresar)
                    guardar_cambios()  # Actualiza saldo en la base de datos
                except ValueError:
                    print("Error: ingrese una cantidad válida\n")

            # Opción 4: Salir del sistema
            elif opcion == "4":
                print("Gracias por usar nuestro cajero. ¡Hasta pronto!\n")
                break

            # Si el usuario introduce una opción no válida
            else:
                print("Opción no válida. Intente de nuevo.\n")

        # Si el usuario sale del menú, se rompe también el bucle de intentos
        break

    else:
        # Si no es válido, muestra error y suma un intento fallido
        print("PIN incorrecto, ingrese el PIN otra vez\n")
        intentos += 1

# Si se superan los 3 intentos fallidos
if intentos == 3:
    print("PIN incorrecto más de 3 veces, entrada denegada\n")

# Cierra la conexión a la base de datos
base_datos.cerrar()


