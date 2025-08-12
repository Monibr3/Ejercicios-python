import getpass   # Para introducir el PIN sin mostrarlo en pantalla
import sqlite3
import Gestión_de_cuentas_bancarias as gb  # Módulo con clases CuentaBancaria y BaseDatos

# Creamos instancia para trabajar con la base de datos
base_datos = gb.BaseDatos()

def guardar_cambios():
    """
    Guarda el saldo actualizado de la cuenta en la base de datos.
    Se llama tras ingresar o retirar dinero.
    """
    base_datos.actualizar_saldo(cuenta.numero_cuenta, cuenta.saldo)


# Contador de intentos fallidos de autenticación
intentos = 0

while intentos < 3:
    # Solicitar datos de acceso
    ncuenta_ingresado = input("Hola, introduzca su número de cuenta:\n").strip()
    pin_ingresado = getpass.getpass("Hola, introduzca su PIN:\n").strip()
    
    # Intentar obtener cuenta desde la base de datos
    cuenta = base_datos.obtener_cuenta(ncuenta_ingresado)
    
    if cuenta and cuenta.verificar_pin(pin_ingresado):
        print("Acceso concedido.\n")
        
        while True:
            print("""
¿Qué operación quiere realizar?
1.- Consultar saldo
2.- Retirar dinero
3.- Ingresar dinero
4.- Consultar transacciones
5.- Salir
""")
            opcion = input("Seleccione una opción (1-5): ").strip()
            
            if opcion == "1":
                print(f"Su saldo actual es de {cuenta.mostrar_saldo()} euros.\n")

            elif opcion == "2":
                try:
                    cantidad = float(input("¿Qué cantidad desea retirar? ").strip())
                    cuenta.retirar(cantidad)
                    guardar_cambios()
                    base_datos.registrar_transaccion(cuenta.numero_cuenta, "Retiro", cantidad)
                    print(f"Retiro de {cantidad} euros realizado.\n")
                except ValueError as e:
                    print(f"Error: {e}\n")

            elif opcion == "3":
                try:
                    cantidad = float(input("¿Qué cantidad desea ingresar? ").strip())
                    cuenta.ingresar(cantidad)
                    guardar_cambios()
                    base_datos.registrar_transaccion(cuenta.numero_cuenta, "Ingreso", cantidad)
                    print(f"Ingreso de {cantidad} euros realizado.\n")
                except ValueError as e:
                    print(f"Error: {e}\n")

            elif opcion == "4":
                transacciones = base_datos.obtener_transacciones(cuenta.numero_cuenta)
                if transacciones:
                    print("Historial de transacciones (más recientes primero):")
                    for tipo, cantidad, fecha in transacciones:
                        print(f"{fecha} - {tipo}: {cantidad} euros")
                    print()
                else:
                    print("No hay transacciones para mostrar.\n")

            elif opcion == "5":
                print("Gracias por usar nuestro cajero. ¡Hasta pronto!\n")
                break

            else:
                print("Opción no válida. Intente de nuevo.\n")

        break  # Salir del bucle de intentos tras sesión exitosa

    else:
        print("Número de cuenta o PIN incorrectos. Intente de nuevo.\n")
        intentos += 1

if intentos == 3:
    print("PIN incorrecto más de 3 veces, entrada denegada.\n")

# Cerramos conexión con la base de datos al terminar
base_datos.cerrar()



