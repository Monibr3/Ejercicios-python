"""
Programa de Gestión de Cuentas Bancarias con Persistencia en SQLite

Este programa permite crear y gestionar cuentas bancarias de manera sencilla
utilizando una base de datos SQLite para almacenar la información de las cuentas.

Funcionalidades principales:
- Crear nuevas cuentas bancarias con titular, número de cuenta, PIN cifrado y saldo inicial.
- Consultar el saldo disponible en una cuenta previa autenticación.
- Ingresar dinero en una cuenta.
- Retirar dinero de una cuenta (si hay saldo suficiente).
- Visualizar el historial de transacciones de una cuenta.
- Salir del programa cerrando la conexión con la base de datos.

Características destacadas:
- Seguridad: El PIN se almacena cifrado usando SHA-256, y se verifica sin revelar el PIN original.
- Integridad: Validaciones para entradas como PIN, saldo y cantidades positivas.
- Registro de transacciones: Cada movimiento se guarda con tipo, cantidad y fecha para auditoría.
- Manejo robusto de errores y una interfaz por consola fácil de usar.

Requiere el módulo 'sqlite3' y un módulo personalizado 'CuentaBancaria' y 'BaseDatos' 
con la lógica de cuentas y persistencia en SQLite.

Nota: El programa es similar al de cajero_avanzado pero mejor extructurado

"""

from Gestión_de_cuentas_bancarias import CuentaBancaria, BaseDatos  # Cambia 'tu_modulo' por el nombre real de tu archivo

def pedir_pin():
    """
    Solicita al usuario que introduzca un PIN válido.
    Un PIN válido es una cadena de 4 dígitos numéricos.
    """
    while True:
        pin = input("Introduce un PIN de 4 dígitos: ")
        if pin.isdigit() and len(pin) == 4:
            return pin
        else:
            print("Error: El PIN debe tener exactamente 4 dígitos numéricos.")

def pedir_numero_cuenta():
    """
    Solicita un número de cuenta no vacío.
    Se asegura que el usuario no deje el campo vacío.
    """
    while True:
        numero = input("Introduce el número de cuenta: ").strip()
        if numero:
            return numero
        else:
            print("Error: El número de cuenta no puede estar vacío.")

def pedir_cantidad(mensaje):
    """
    Solicita una cantidad numérica positiva.
    El parámetro 'mensaje' es el texto que se muestra al usuario.
    """
    while True:
        try:
            cantidad = float(input(mensaje))
            if cantidad > 0:
                return cantidad
            else:
                print("Error: La cantidad debe ser un número positivo.")
        except ValueError:
            print("Error: Introduce un número válido.")

def autenticar_cuenta(db):
    """
    Pide el número de cuenta y el PIN para autenticar la cuenta.
    Retorna un objeto CuentaBancaria si la autenticación es exitosa,
    o None si la cuenta no existe o el PIN es incorrecto.
    """
    numero = pedir_numero_cuenta()
    cuenta = db.obtener_cuenta(numero)
    if not cuenta:
        print("Cuenta no encontrada.")
        return None
    pin = pedir_pin()
    if cuenta.verificar_pin(pin):
        return cuenta
    else:
        print("PIN incorrecto.")
        return None

def crear_cuenta(db):
    """
    Permite crear una nueva cuenta bancaria.
    Verifica que el número de cuenta no exista,
    solicita los datos necesarios, valida y almacena la cuenta.
    """
    print("\n--- Crear cuenta bancaria ---")
    numero = pedir_numero_cuenta()
    if db.existe_cuenta(numero):
        print("Error: Ya existe una cuenta con ese número.")
        return
    titular = input("Titular de la cuenta: ").strip()
    pin = pedir_pin()
    saldo = 0
    while True:
        try:
            saldo = float(input("Saldo inicial (>= 0): "))
            if saldo >= 0:
                break
            else:
                print("El saldo no puede ser negativo.")
        except ValueError:
            print("Introduce un número válido.")
    try:
        cuenta = CuentaBancaria(titular, pin, numero, saldo)
        db.insertar_cuenta(cuenta)
        if saldo > 0:
            db.registrar_transaccion(numero, "Ingreso inicial", saldo)
        print("Cuenta creada con éxito.")
    except Exception as e:
        print(f"Error al crear la cuenta: {e}")

def mostrar_saldo(db):
    """
    Permite al usuario consultar el saldo de su cuenta previa autenticación.
    """
    print("\n--- Consulta de saldo ---")
    cuenta = autenticar_cuenta(db)
    if cuenta:
        print(f"Titular: {cuenta.titular}")
        print(f"Saldo actual: {cuenta.mostrar_saldo():.2f}")

def ingresar_dinero(db):
    """
    Permite ingresar dinero en una cuenta tras autenticarse.
    Actualiza la base de datos y registra la transacción.
    """
    print("\n--- Ingresar dinero ---")
    cuenta = autenticar_cuenta(db)
    if cuenta:
        cantidad = pedir_cantidad("Cantidad a ingresar: ")
        try:
            cuenta.ingresar(cantidad)
            db.actualizar_saldo(cuenta.numero_cuenta, cuenta.saldo)
            db.registrar_transaccion(cuenta.numero_cuenta, "Ingreso", cantidad)
            print(f"Ingreso realizado. Nuevo saldo: {cuenta.saldo:.2f}")
        except Exception as e:
            print(f"Error al ingresar dinero: {e}")

def retirar_dinero(db):
    """
    Permite retirar dinero de una cuenta tras autenticarse.
    Verifica saldo suficiente, actualiza la base de datos y registra la transacción.
    """
    print("\n--- Retirar dinero ---")
    cuenta = autenticar_cuenta(db)
    if cuenta:
        cantidad = pedir_cantidad("Cantidad a retirar: ")
        try:
            cuenta.retirar(cantidad)
            db.actualizar_saldo(cuenta.numero_cuenta, cuenta.saldo)
            db.registrar_transaccion(cuenta.numero_cuenta, "Retiro", cantidad)
            print(f"Retiro realizado. Nuevo saldo: {cuenta.saldo:.2f}")
        except Exception as e:
            print(f"Error al retirar dinero: {e}")

def mostrar_transacciones(db):
    """
    Muestra el historial de transacciones de una cuenta tras autenticación.
    Lista tipo, cantidad y fecha de cada movimiento.
    """
    print("\n--- Historial de transacciones ---")
    cuenta = autenticar_cuenta(db)
    if cuenta:
        transacciones = db.obtener_transacciones(cuenta.numero_cuenta)
        if transacciones:
            print(f"Transacciones para la cuenta {cuenta.numero_cuenta}:")
            for tipo, cantidad, fecha in transacciones:
                print(f"{fecha} - {tipo}: {cantidad:.2f}")
        else:
            print("No hay transacciones registradas.")

def menu():
    """
    Muestra el menú principal de opciones para el usuario.
    """
    print("""
=== Menú de gestión bancaria ===
1. Crear cuenta
2. Consultar saldo
3. Ingresar dinero
4. Retirar dinero
5. Mostrar historial de transacciones
6. Salir
""")

def main():
    """
    Función principal que controla el flujo del programa.
    Crea la base de datos y muestra el menú hasta que el usuario decida salir.
    """
    db = BaseDatos("banco.db")  # Inicializa la conexión a la base de datos
    while True:
        menu()
        opcion = input("Selecciona una opción (1-6): ")
        if opcion == "1":
            crear_cuenta(db)
        elif opcion == "2":
            mostrar_saldo(db)
        elif opcion == "3":
            ingresar_dinero(db)
        elif opcion == "4":
            retirar_dinero(db)
        elif opcion == "5":
            mostrar_transacciones(db)
        elif opcion == "6":
            print("Saliendo del programa...")
            db.cerrar()
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
