# Programa que gestiona una lista de tareas que se encuentra en un archivo de texto

# Función que lee todas las tareas del archivo y las devuelve como una lista
def leer_lista_tareas():
    with open("Tareas.txt","r") as archivo:
        tareas = archivo.readlines()  # Lee todas las líneas del archivo y las guarda en una lista
        return tareas  # Devuelve la lista de tareas

# Función que muestra las tareas en pantalla, con su número correspondiente
def mostrar_tareas():
    tareas = leer_lista_tareas()  # Obtiene la lista de tareas desde el archivo
    if not tareas:  # Si la lista está vacía
        print("No hay tareas guardadas.")
    else:
        print("\nLista de tareas:")
        for i, tarea in enumerate(tareas, 1):  # Recorre la lista y numera desde 1
            print(f"{i}.{tarea.strip()}")  # Muestra el número y la tarea (sin salto de línea)

# Función para crear nuevas tareas y guardarlas en el archivo
def crear_lista_tareas_con_indice():
    try:
        tareas = leer_lista_tareas()  # Intenta leer las tareas para saber cuántas hay
        indice = len(tareas) + 1  # Calcula el nuevo índice (aunque no se usa luego)
    except FileNotFoundError:  # Si el archivo no existe, empieza sin tareas
        tareas = []

    # Abre el archivo en modo 'append' para añadir tareas al final
    with open("Tareas.txt", "a") as archivo:
        while True:
            tarea = input("Introduce una tarea: ")  # Pide una nueva tarea al usuario
            archivo.write(f"{tarea}\n")  # Escribe la tarea en el archivo con salto de línea
            otra = input("¿Quieres introducir otra tarea? (s/n): ").lower()  # Pregunta si quiere continuar
            if otra != 's':  # Si no es 's', sale del bucle
                break

# Función para borrar una tarea seleccionada por el usuario
def borrar_tarea():
    tareas = leer_lista_tareas()  # Lee todas las tareas del archivo
    if not tareas:  # Si no hay tareas
        print("No hay tareas para eliminar.")
        return  # Sale de la función

    mostrar_tareas()  # Muestra la lista actual para que el usuario vea los números
    num = int(input("Introduce que tarea deseas eliminar \n"))  # Pide el número de tarea a eliminar

    try:
        if 1 <= num <= len(tareas):  # Comprueba que el número está dentro del rango válido
            eliminada = tareas.pop(num - 1)  # Elimina la tarea correspondiente (resta 1 por índice de lista)
            with open("Tareas.txt", "w") as archivo:
                archivo.writelines(tareas)  # Sobrescribe el archivo con las tareas restantes
            print(f"Tarea eliminada: {eliminada.strip()}")  # Informa al usuario cuál fue eliminada
        else:
            print("Número fuera de rango.")  # Si el número no es válido
    except ValueError:
        print("Entrada inválida. Introduce un número válido.")  # Si se introduce algo que no es número

def editar_tarea():
    tareas = leer_lista_tareas()  # Leer todas las tareas actuales

    if not tareas:
        print("No hay tareas para editar.")
        return

    mostrar_tareas()  # Mostrar tareas con número

    try:
        num = int(input("\nIntroduce el número de la tarea que quieres editar: "))
        if 1 <= num <= len(tareas):
            nueva_tarea = input("Escribe la nueva descripción de la tarea: ")
            tareas[num - 1] = nueva_tarea + "\n"  # Reemplaza la tarea
            with open("Tareas.txt", "w") as archivo:
                archivo.writelines(tareas)  # Sobrescribe todo el archivo
            print("Tarea actualizada correctamente.")
        else:
            print("Número fuera de rango.")
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número válido.")

# Variable para controlar la opción seleccionada por el usuario
opcion = 0

# Bucle principal del menú. Se repite hasta que se elige la opción 4 (salir)
while opcion != 5:
    print("\n---MENÚ DE ACCIONES---")
    print("1.-Introducir tarea")
    print("2.-Lista de tareas")
    print("3.-Borrar tarea")
    print("4.-Editar tarea")
    print("5.-Salir")
    try:
        opcion = int(input("Elige una opción (1-5): "))  # Se pide al usuario una opción
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número del 1 al 5.")
        continue  # Si no es un número, vuelve a mostrar el menú

    if opcion < 1 or opcion > 4:  # Si el número está fuera de las opciones válidas
        print("Opción incorrecta. Inténtalo de nuevo.")
    elif opcion == 1:
        crear_lista_tareas_con_indice()  # Añadir nuevas tareas
    elif opcion == 2:
        mostrar_tareas()  # Mostrar la lista actual
    elif opcion == 3:
        borrar_tarea()  # Eliminar una tarea
    elif opcion == 4:
        editar_tarea()  # Editar una tarea    
    elif opcion == 5:
        print("¡Hasta luego!")  # Salida del programa
    else:
        print("Opción incorrecta. Inténtalo de nuevo.")  # No debería ejecutarse si todo está correcto