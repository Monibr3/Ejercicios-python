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

import hashlib  # Para cifrar el PIN

class CuentaBancaria:
    def __init__(self, titular, pin, numero_cuenta, saldo=0):
        # Validar que el PIN sea una cadena de 4 dígitos numéricos
        if not (isinstance(pin, str) and pin.isdigit() and len(pin) == 4):
            raise ValueError("El PIN debe ser una cadena de 4 dígitos numéricos")
        
        # Validar que el saldo inicial no sea negativo
        if saldo < 0:
            raise ValueError("El saldo inicial no puede ser negativo")

        self.titular = titular
        self.pin = self.cifrar_pin(pin)
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo
        
    def cifrar_pin(self, pin):
        """Devuelve el hash SHA-256 del PIN."""
        return hashlib.sha256(pin.encode()).hexdigest()    
    
    def verificar_pin(self, pin_introducido):
        """Comprueba si el PIN introducido es correcto."""
        return self.pin == self.cifrar_pin(pin_introducido)


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
        try:
            self.conn = sqlite3.connect(nombre_db)
            self.cursor = self.conn.cursor()
            self.crear_tabla_cuentas()
            self.crear_tabla_transacciones()
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise

    def crear_tabla_cuentas(self):
        # Crea la tabla 'cuentas' si no existe, con columnas para número de cuenta, PIN, titular y saldo
        
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cuentas (
                    numero_cuenta TEXT PRIMARY KEY,
                    pin TEXT,
                    titular TEXT,
                    saldo REAL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tabla cuentas: {e}")
            raise

    def existe_cuenta(self, numero_cuenta):
            # Comprueba si una cuenta con el número dado existe en la base de datos
            try:
                self.cursor.execute(
                    "SELECT 1 FROM cuentas WHERE numero_cuenta = ?",
                    (numero_cuenta,)
                )
                return self.cursor.fetchone() is not None
            except sqlite3.Error as e:
                print(f"Error al consultar cuenta: {e}")
                raise
        
    def insertar_cuenta(self, cuenta: CuentaBancaria):
        # Inserta una nueva cuenta en la base de datos si no existe previamente
        try:
            if self.existe_cuenta(cuenta.numero_cuenta):
                raise ValueError(f"La cuenta {cuenta.numero_cuenta} ya existe.")
            self.cursor.execute(
                "INSERT INTO cuentas (numero_cuenta, pin, titular, saldo) VALUES (?, ?, ?, ?)",
                (cuenta.numero_cuenta, cuenta.pin, cuenta.titular, cuenta.saldo)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar cuenta: {e}")
            raise

    def obtener_cuenta(self, numero_cuenta):
        # Recupera una cuenta desde la base de datos y devuelve un objeto CuentaBancaria
        try:
            self.cursor.execute(
                "SELECT numero_cuenta, pin, titular, saldo FROM cuentas WHERE numero_cuenta = ?",
                (numero_cuenta,)
            )
            fila = self.cursor.fetchone()
            if fila:
                cuenta = CuentaBancaria(titular=fila[2], pin="0000", numero_cuenta=fila[0], saldo=fila[3])
                # Al recuperar, asignamos el PIN cifrado directamente (no lo ciframos otra vez)
                cuenta.pin = fila[1]
                return cuenta
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener cuenta: {e}")
            raise

    def actualizar_saldo(self, numero_cuenta, nuevo_saldo):
        # Actualiza el saldo de una cuenta en la base de datos
        try:
            self.cursor.execute(
                "UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?",
                (nuevo_saldo, numero_cuenta)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al actualizar saldo: {e}")
            raise

    def cerrar(self):
        # Cierra la conexión a la base de datos
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error al cerrar la base de datos: {e}")
            raise
    
    def crear_tabla_transacciones(self):
        # Crea la tabla 'transacciones' si no existe, para almacenar cada movimiento
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transacciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_cuenta TEXT,
                    tipo TEXT,
                    cantidad REAL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(numero_cuenta) REFERENCES cuentas(numero_cuenta)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tabla transacciones: {e}")
            raise

    def registrar_transaccion(self, numero_cuenta, tipo, cantidad):
        # Inserta una transacción en la tabla con la fecha automática
        try:
            self.cursor.execute("""
                INSERT INTO transacciones (numero_cuenta, tipo, cantidad) 
                VALUES (?, ?, ?)
            """, (numero_cuenta, tipo, cantidad))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar transacción: {e}")
            raise

    def obtener_transacciones(self, numero_cuenta):
        # Obtiene todas las transacciones para una cuenta ordenadas de más recientes a más antiguas
        try:
            self.cursor.execute("""
                SELECT tipo, cantidad, fecha FROM transacciones 
                WHERE numero_cuenta = ? ORDER BY fecha DESC
            """, (numero_cuenta,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener transacciones: {e}")
            raise