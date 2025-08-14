# Importamos la clase Contacto y el gestor de la agenda
from contacto_agenda import Contacto
from gestor_agenda import GestorAgenda

# Función para pedir todos los datos necesarios para crear un contacto
def pedir_datos_contacto():
    try:
        # Pedimos cada dato al usuario y eliminamos espacios en blanco al principio y al final
        id_contacto = input("ID del contacto: ").strip()
        nombre = input("Nombre: ").strip()
        telefono = input("Teléfono: ").strip()
        direccion = input("Dirección: ").strip()
        correo = input("Correo: ").strip()
        notas = input("Notas (opcional): ").strip()

        # Creamos un objeto Contacto con los datos introducidos
        contacto = Contacto(id_contacto, nombre, telefono, direccion, correo, notas)
        return contacto  # Devolvemos el contacto creado

    except ValueError as e:
        # Captura errores específicos, como correo inválido
        print(f"Error: {e}")
        return None

    except Exception as e:
        # Captura cualquier otro error inesperado
        print(f"Error al introducir los datos: {e}")
        return None

# Función que muestra el menú principal y devuelve la opción elegida por el usuario
def mostrar_menu():
    print("\n--- AGENDA ELECTRÓNICA ---")
    print("1. Añadir contacto")
    print("2. Buscar contacto por ID")
    print("3. Eliminar contacto por ID")
    print("4. Listar todos los contactos")
    print("5. Modificar contacto")
    print("6. Buscar contactos por texto")
    print("7. Marcar contacto como favorito")
    print("8. Desmarcar contacto como favorito")
    print("9. Salir")
    return input("Elige una opción: ")

# Función principal que controla el flujo del programa
def main():
    # Creamos un gestor de agenda para manejar los contactos
    agenda = GestorAgenda()

    # Bucle infinito hasta que el usuario decida salir
    while True:
        try:
            # Mostramos el menú y pedimos la opción
            opcion = mostrar_menu()

            # --- Añadir contacto ---
            if opcion == "1":
                contacto = pedir_datos_contacto()
                if contacto:
                    agenda.añadir_contacto(contacto)
                    print("Contacto añadido con éxito.")

            # --- Buscar contacto por ID ---
            elif opcion == "2":
                id_buscar = input("Introduce el ID del contacto: ").strip()
                contacto = agenda.buscar_contacto_por_id(id_buscar)
                if contacto:
                    contacto.mostrar_contacto()
                else:
                    print("Contacto no encontrado.")

            # --- Eliminar contacto por ID ---
            elif opcion == "3":
                id_eliminar = input("Introduce el ID del contacto a eliminar: ").strip()
                if agenda.eliminar_contacto(id_eliminar):
                    print("Contacto eliminado.")
                else:
                    print("No se encontró el contacto.")

            # --- Listar todos los contactos ---
            elif opcion == "4":
                contactos = agenda.listar_contactos()
                if contactos:
                    for c in contactos:
                        c.mostrar_contacto()
                        print("-" * 20)  # Separador visual entre contactos
                else:
                    print("No hay contactos en la agenda.")

            # --- Modificar contacto ---
            elif opcion == "5":
                id_mod = input("ID del contacto a modificar: ").strip()
                contacto_actual = agenda.buscar_contacto_por_id(id_mod)
                if contacto_actual:
                    print("Introduce los nuevos datos del contacto (pulsa Enter para mantener el valor actual):")
                    
                    # Pedimos cada dato, mostrando el valor actual
                    nombre = input(f"Nombre [{contacto_actual.nombre}]: ").strip()
                    if not nombre:
                        nombre = contacto_actual.nombre  # mantener valor actual

                    telefono = input(f"Teléfono [{contacto_actual.telefono}]: ").strip()
                    if not telefono:
                        telefono = contacto_actual.telefono

                    direccion = input(f"Dirección [{contacto_actual.direccion}]: ").strip()
                    if not direccion:
                        direccion = contacto_actual.direccion

                    correo = input(f"Correo [{contacto_actual.correo}]: ").strip()
                    if not correo:
                        correo = contacto_actual.correo
                    else:
                        # Validamos el correo nuevo
                        if not Contacto.validar_correo(contacto_actual, correo):
                            print(f"Correo inválido: {correo}")
                            correo = contacto_actual.correo  # mantener valor anterior

                    notas = input(f"Notas [{contacto_actual.notas}]: ").strip()
                    if not notas:
                        notas = contacto_actual.notas

                    # Creamos un nuevo contacto con los datos actualizados
                    contacto_nuevo = Contacto(
                        id_contacto=contacto_actual.id_contacto,
                        nombre=nombre,
                        telefono=telefono,
                        direccion=direccion,
                        correo=correo,
                        notas=notas
                    )
                    # Mantenemos el estado de favorito
                    contacto_nuevo.favorito = contacto_actual.favorito

                    if agenda.modificar_contacto(id_mod, contacto_nuevo):
                        print("Contacto modificado.")
                    else:
                        print("No se pudo modificar el contacto.")
                else:
                    print("No se encontró el contacto.")

            # --- Buscar contactos por texto ---
            elif opcion == "6":
                texto = input("Introduce parte del nombre, teléfono o correo: ").strip()
                encontrados = agenda.buscar_contactos_por_texto(texto)
                if encontrados:
                    for c in encontrados:
                        c.mostrar_contacto()
                        print("-" * 20)
                else:
                    print("No se encontraron coincidencias.")

            # --- Marcar contacto como favorito ---
            elif opcion == "7":
                id_fav = input("ID del contacto a marcar como favorito: ").strip()
                if agenda.marcar_favorito(id_fav):
                    print("Contacto marcado como favorito.")
                else:
                    print("No se encontró el contacto.")

            # --- Desmarcar contacto como favorito ---
            elif opcion == "8":
                id_no_fav = input("ID del contacto a desmarcar como favorito: ").strip()
                if agenda.desmarcar_favorito(id_no_fav):
                    print("Contacto desmarcado como favorito.")
                else:
                    print("No se encontró el contacto.")

            # --- Salir del programa ---
            elif opcion == "9":
                print("¡Hasta luego!")
                break

            # --- Opción no válida ---
            else:
                print("Opción no válida, prueba otra vez.")

        except Exception as e:
            # Captura cualquier error inesperado durante la ejecución del menú
            print(f"Ocurrió un error inesperado: {e}")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
