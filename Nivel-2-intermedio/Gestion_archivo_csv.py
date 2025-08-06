# Programa para gestionar archivos CSV mediante un menú interactivo.
# Permite crear, mostrar, modificar y borrar filas de un archivo CSV.

import os  # Módulo para operaciones del sistema de archivos
import csv  # Módulo para trabajar con archivos CSV (lectura/escritura)

# ----------------------- FUNCIÓN 1 -----------------------
# Verifica si el archivo existe. Si no existe, lo crea y solicita los campos de cabecera.
def verificar_o_crear_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):  # Verifica si el archivo no existe
        campos = input("Introduce los campos (separados por comas): ").strip().split(",")  # Pide los campos
        with open(nombre_archivo, "w", newline="") as archivo:
            escritor = csv.writer(archivo)  # Crea un escritor CSV
            escritor.writerow([campo.strip() for campo in campos])  # Escribe la fila de cabecera
        print(f"Archivo {nombre_archivo} creado con los campos: {', '.join(campos)}")
    else:
        print("El archivo ya existe.")

# ----------------------- FUNCIÓN 2 -----------------------
# Lee y devuelve la cabecera (campos) del archivo CSV
def leer_campos(nombre_archivo):
    with open(nombre_archivo, "r", newline="") as archivo:
        lector = csv.reader(archivo)  # Crea un lector CSV
        campos = next(lector)  # Lee la primera fila (cabecera)
        return campos

# ----------------------- FUNCIÓN 3 -----------------------
# Añade una nueva fila de datos al archivo CSV
def añadir_fila(nombre_archivo):
    campos = leer_campos(nombre_archivo)  # Obtiene los nombres de los campos
    datos = []  # Lista para almacenar los valores ingresados
    print("Introduce datos para cada campo:")
    for campo in campos:
        valor = input(f"{campo}: ").strip()  # Solicita el valor para cada campo
        datos.append(valor)
    with open(nombre_archivo, "a", newline="") as archivo:
        escritor = csv.writer(archivo)  # Crea un escritor CSV en modo añadir
        escritor.writerow(datos)  # Escribe la nueva fila
    print("Datos añadidos correctamente.")

# ----------------------- FUNCIÓN 4 -----------------------
# Lee todo el contenido del archivo y lo devuelve como lista de listas
def obtener_datos_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):  # Verifica si el archivo no existe
        return None
    with open(nombre_archivo, "r", newline="") as archivo:
        lector = list(csv.reader(archivo))  # Convierte el lector en una lista completa
    return lector

# ----------------------- FUNCIÓN 5 -----------------------
# Muestra por pantalla el contenido completo del archivo CSV
def mostrar_archivo(nombre_archivo):
    datos = obtener_datos_archivo(nombre_archivo)
    if datos is None:
        print(f"El archivo {nombre_archivo} no existe.")
        return
    if len(datos) == 0:
        print("El archivo está vacío")
        return
    print("\nContenido del archivo:")
    for i, fila in enumerate(datos):  # Muestra cada fila numerada
        print(f"{i+1}: {', '.join(fila)}")

# ----------------------- FUNCIÓN 6 -----------------------
# Permite al usuario borrar una fila específica del archivo CSV
def borrar_fila(nombre_archivo):
    datos = obtener_datos_archivo(nombre_archivo)
    if datos is None:
        print(f"El archivo {nombre_archivo} no existe.")
        return
    if len(datos) == 0 or not datos[0]:  # Verifica si está vacío o sin cabecera
        print("El archivo está vacío o mal formado.")
        return
    print("\nFilas disponibles para borrar:")
    for i, linea in enumerate(datos[1:], start=1):  # Muestra las filas (excepto cabecera)
        print(f"{i}: {', '.join(linea)}")

    try:
        num = int(input("Introduce la fila que deseas eliminar: "))  # Solicita la fila a borrar
        if 1 <= num <= len(datos) - 1:
            eliminada = datos.pop(num)  # Elimina la fila seleccionada
            with open(nombre_archivo, "w", newline="") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerows(datos)  # Reescribe el archivo sin esa fila
            print(f"Fila eliminada: {', '.join(eliminada)}")
        else:
            print("Número fuera de rango.")
    except ValueError:
        print("Entrada inválida. Introduce un número válido.")

# ----------------------- FUNCIÓN 7 -----------------------
# Permite modificar una fila existente en el archivo CSV
def modificar_fila(nombre_archivo):
    datos = obtener_datos_archivo(nombre_archivo)
    if datos is None:
        print(f"El archivo {nombre_archivo} no existe.")
        return
    if len(datos) <= 1:  # Solo tiene cabecera o está vacío
        print("No hay datos para modificar.")
        return
    print("\nFilas disponibles para modificar:")
    for i, linea in enumerate(datos[1:], start=1):  # Muestra las filas sin incluir la cabecera
        print(f"{i}: {', '.join(linea)}")

    try:
        num = int(input("Introduce la fila que deseas modificar: "))  # Solicita la fila a modificar
        if 1 <= num <= len(datos) - 1:
            fila = datos[num]  # Toma la fila a modificar
            campos = datos[0]  # Cabecera (nombres de campos)
            print("Introduce los nuevos datos. Deja vacío para mantener el valor actual.")
            for i, campo in enumerate(campos):
                valor_actual = fila[i]
                nuevo_valor = input(f"{campo} (actual: {valor_actual}): ").strip()
                if nuevo_valor:  # Si se ingresa algo nuevo, se reemplaza
                    fila[i] = nuevo_valor
            datos[num] = fila  # Actualiza la fila en la lista de datos
            with open(nombre_archivo, "w", newline="") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerows(datos)  # Escribe todos los datos de nuevo
            print("Fila modificada correctamente.")
        else:
            print("Número fuera de rango.")
    except ValueError:
        print("Entrada inválida. Introduce un número válido.")

# ----------------------- FUNCIÓN AUXILIAR -----------------------
# Asegura que el nombre del archivo tenga la extensión .csv
def asegurar_extension_csv(nombre):
    return nombre if nombre.endswith(".csv") else nombre + ".csv"

# ----------------------- MENÚ PRINCIPAL -----------------------

opcion = 0  # Variable para controlar el bucle del menú

# Bucle del menú que se repite hasta que el usuario elige salir (opción 6)
while opcion != 6:
    print("\n--- MENÚ DE ACCIONES ---")
    print("1.- Crear Archivo CSV")
    print("2.- Añadir datos")
    print("3.- Mostrar datos")
    print("4.- Borrar Datos")
    print("5.- Editar Datos")
    print("6.- Salir")
    try:
        opcion = int(input("Elige una opción (1-6): "))  # Entrada del usuario
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número del 1 al 6.")
        continue

    # Verifica si la opción está en el rango válido
    if opcion < 1 or opcion > 6:
        print("Opción incorrecta. Inténtalo de nuevo.")
        continue

    # Procesa la opción seleccionada
    elif opcion == 1:
        nombre = asegurar_extension_csv(input("Introduce el nombre del archivo que quieres crear: "))
        verificar_o_crear_archivo(nombre)
    elif opcion == 2:
        nombre = asegurar_extension_csv(input("Introduce el nombre del archivo al que quieres añadir datos: "))
        añadir_fila(nombre)
    elif opcion == 3:
        nombre = asegurar_extension_csv(input("Introduce el nombre del archivo que quieres ver: "))
        mostrar_archivo(nombre)
    elif opcion == 4:
        nombre = asegurar_extension_csv(input("Introduce el nombre del archivo del que quieres borrar datos: "))
        borrar_fila(nombre)
    elif opcion == 5:
        nombre = asegurar_extension_csv(input("Introduce el nombre del archivo que quieres modificar: "))
        modificar_fila(nombre)
    elif opcion == 6:
        print("¡Hasta luego!")  # Mensaje de despedida

