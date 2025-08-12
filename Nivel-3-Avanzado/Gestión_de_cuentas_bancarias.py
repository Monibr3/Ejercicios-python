# Módulo de gestión de cuentas bancarias con persistencia en SQLite
# -----------------------------------------------------------------
# Este módulo define dos clases principales:
# 
# 1. CuentaBancaria:
#    Representa una cuenta bancaria con atributos como titular, PIN, número de cuenta y saldo.
#    Incluye métodos para verificar el PIN, ingresar dinero, retirar dinero y mostrar saldo.
#    Implementa validaciones para garantizar integridad de datos, como PIN de 4 dígitos y saldo positivo.
#
# 2. BaseDatos:
#    Maneja la conexión con una base de datos SQLite para almacenar la información de las cuentas.
#    Permite crear la tabla de cuentas si no existe, insertar nuevas cuentas, obtener cuentas por número,
#    actualizar el saldo de una cuenta, y cerrar la conexión.
#
# Este diseño permite separar la lógica de la cuenta de la persistencia, facilitando su mantenimiento y ampliación.
# Se basa en buenas prácticas como el uso de excepciones para validar entradas y asegurar la integridad.
#
# La base de datos utiliza un esquema simple con columnas para número de cuenta (clave primaria), PIN, titular y saldo.
# Los métodos de BaseDatos realizan commits para asegurar que los cambios se guarden permanentemente.

import sqlite3


class CuentaBancaria:
    def __init__(self, titular, pin, numero_cuenta, saldo=0):
        # Validar que el PIN sea una cadena de 4 dígitos numéricos
        if not (isinstance(pin, str) and pin.isdigit() and len(pin) == 4):
            raise ValueError("El PIN debe ser una cadena de 4 dígitos numéricos")
        
        # Validar que el saldo inicial no sea negativo
        if saldo < 0:
            raise ValueError("El saldo inicial no puede ser negativo")

        self.titular = titular
        self.pin = pin
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo
        
    def verificar_pin(self, pin_introducido):
        """Comprueba si el PIN introducido es correcto."""
        return self.pin == pin_introducido

    def ingresar(self, cantidad):
        """Ingresa dinero en la cuenta."""
        if cantidad <= 0:
            raise ValueError("La cantidad a ingresar debe ser positiva")
        self.saldo += cantidad
    
    def retirar(self, cantidad):
        """Retira dinero de la cuenta si hay saldo suficiente."""
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser positiva")
        if cantidad > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= cantidad

    def mostrar_saldo(self):
        """Devuelve el saldo actual."""
        return self.saldo


class BaseDatos:
    def __init__(self, nombre_db="banco.db"):
        # Establece conexión con la base de datos SQLite
        self.conn = sqlite3.connect(nombre_db)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        # Crea la tabla 'cuentas' si no existe, con columnas para número de cuenta, PIN, titular y saldo
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuentas (
                num_cuenta TEXT PRIMARY KEY,
                pin TEXT,
                titular TEXT,
                saldo REAL
            )
        """)
        self.conn.commit()

    def existe_cuenta(self, numero_cuenta):
        # Comprueba si una cuenta con el número dado existe en la base de datos
        self.cursor.execute(
            "SELECT 1 FROM cuentas WHERE numero_cuenta = ?",
            (numero_cuenta,)
        )
        return self.cursor.fetchone() is not None
    
    def insertar_cuenta(self, cuenta: CuentaBancaria):
        # Inserta una nueva cuenta en la base de datos si no existe previamente
        if self.existe_cuenta(cuenta.numero_cuenta):
            raise ValueError(f"La cuenta {cuenta.numero_cuenta} ya existe.")
        self.cursor.execute(
            "INSERT INTO cuentas (numero_cuenta, pin, titular, saldo) VALUES (?, ?, ?, ?)",
            (cuenta.numero_cuenta, cuenta.pin, cuenta.titular, cuenta.saldo)
        )
        self.conn.commit()

    def obtener_cuenta(self, numero_cuenta):
        # Recupera una cuenta desde la base de datos y devuelve un objeto CuentaBancaria
        self.cursor.execute(
            "SELECT numero_cuenta, pin, titular, saldo FROM cuentas WHERE numero_cuenta = ?",
            (numero_cuenta,)
        )
        fila = self.cursor.fetchone()
        if fila:
            return CuentaBancaria(titular=fila[2], pin=fila[1], numero_cuenta=fila[0], saldo=fila[3])
        else:
            return None

    def actualizar_saldo(self, numero_cuenta, nuevo_saldo):
        # Actualiza el saldo de una cuenta en la base de datos
        self.cursor.execute(
            "UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?",
            (nuevo_saldo, numero_cuenta)
        )
        self.conn.commit()

    def cerrar(self):
        # Cierra la conexión a la base de datos
        self.conn.close()