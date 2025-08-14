import json
from contacto_agenda import Contacto  # Importa la clase Contacto desde otro archivo


class GestorAgenda:
    """
    Esta clase se encarga de gestionar todos los contactos de la agenda.
    Permite:
    - Añadir, eliminar y modificar contactos
    - Buscar contactos por ID o por texto
    - Listar todos los contactos
    - Marcar y desmarcar favoritos
    La información se guarda en un archivo JSON para mantenerla entre ejecuciones.
    """

    def __init__(self, archivo_json="agenda.json"):
        """
        Método constructor que se ejecuta al crear un objeto GestorAgenda.
        
        Parámetros:
        archivo_json: nombre del archivo donde se guardarán los contactos (por defecto "agenda.json").
        
        Lo que hace:
        1. Guarda el nombre del archivo en un atributo.
        2. Inicializa una lista vacía que contendrá todos los contactos.
        3. Llama a 'cargar_contactos' para cargar los contactos existentes del archivo JSON.
        """
        self.archivo_json = archivo_json
        self.contactos = []  # Aquí se guardarán los objetos Contacto
        self.cargar_contactos()  # Carga los contactos guardados previamente

    def cargar_contactos(self):
        """
        Carga los contactos desde el archivo JSON.
        
        Cómo funciona:
        1. Intenta abrir el archivo JSON y leer los datos.
        2. Convierte cada diccionario (cada contacto) en un objeto Contacto usando 'from_dict'.
        3. Maneja errores:
           - Si el archivo no existe, se deja la lista vacía.
           - Si el archivo está corrupto, se avisa y se deja la lista vacía.
           - Cualquier otro error se muestra en pantalla.
        """
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)  # Carga los datos del archivo JSON en formato de lista de diccionarios
                self.contactos = [Contacto.from_dict(c) for c in datos]  # Convierte cada diccionario en un objeto Contacto
        except FileNotFoundError:
            # Si el archivo no existe, empezamos con una agenda vacía
            self.contactos = []
        except json.JSONDecodeError:
            # Si el archivo existe pero está corrupto, avisamos y dejamos la agenda vacía
            print("Error: el archivo JSON está corrupto. Se cargará agenda vacía.")
            self.contactos = []
        except Exception as e:
            # Captura cualquier otro error inesperado
            print(f"Ocurrió un error inesperado al cargar contactos: {e}")
            self.contactos = []

    def guardar_contactos(self):
        """
        Guarda la lista de contactos en el archivo JSON.
        
        Cómo funciona:
        1. Convierte cada objeto Contacto en un diccionario usando 'to_dict'.
        2. Escribe la lista de diccionarios en el archivo JSON con formato legible.
        3. Si ocurre un error al guardar, lo muestra por pantalla.
        """
        try:
            with open(self.archivo_json, "w", encoding="utf-8") as f:
                json.dump([c.to_dict() for c in self.contactos], f, indent=4)
        except Exception as e:
            print(f"No se pudo guardar la agenda: {e}")

    def añadir_contacto(self, contacto):
        """
        Añade un contacto a la agenda.
        
        Parámetros:
        contacto: objeto de la clase Contacto que se quiere añadir.
        
        Qué hace:
        1. Añade el contacto a la lista.
        2. Guarda la lista actualizada en el archivo JSON.
        3. Captura errores si algo sale mal.
        """
        try:
            self.contactos.append(contacto)  # Añade el contacto a la lista
            self.guardar_contactos()  # Guarda los cambios en el archivo
        except Exception as e:
            print(f"Error al añadir contacto: {e}")

    def eliminar_contacto(self, id_contacto):
        """
        Elimina un contacto por su ID.
        
        Parámetros:
        id_contacto: número o cadena que identifica unívocamente al contacto.
        
        Qué hace:
        1. Comprueba si existe el contacto.
        2. Lo elimina de la lista si existe.
        3. Guarda los cambios en el archivo JSON.
        4. Devuelve True si se eliminó, False si no se encontró.
        """
        try:
            original = len(self.contactos)  # Guarda el número original de contactos
            # Filtra todos los contactos que NO tengan el ID especificado
            self.contactos = [c for c in self.contactos if c.id_contacto != id_contacto]
            if len(self.contactos) < original:  # Si la lista se redujo, significa que se eliminó un contacto
                self.guardar_contactos()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar contacto: {e}")
            return False

    def modificar_contacto(self, id_contacto, nuevos_datos: Contacto):
        """
        Modifica los datos de un contacto existente.
        
        Parámetros:
        id_contacto: ID del contacto que queremos modificar.
        nuevos_datos: objeto Contacto con los datos actualizados.
        
        Qué hace:
        1. Busca el contacto por ID.
        2. Reemplaza sus datos por los nuevos.
        3. Guarda los cambios en el archivo JSON.
        4. Devuelve True si se modificó, False si no se encontró.
        """
        try:
            for i, c in enumerate(self.contactos):
                if c.id_contacto == id_contacto:
                    self.contactos[i] = nuevos_datos
                    self.guardar_contactos()
                    return True
            return False
        except Exception as e:
            print(f"Error al modificar contacto: {e}")
            return False

    def buscar_contacto_por_id(self, id_contacto):
        """
        Busca un contacto por su ID.
        
        Parámetros:
        id_contacto: ID del contacto que queremos encontrar.
        
        Qué devuelve:
        - El objeto Contacto si se encuentra.
        - None si no existe.
        """
        try:
            for c in self.contactos:
                if c.id_contacto == id_contacto:
                    return c
            return None
        except Exception as e:
            print(f"Error al buscar contacto: {e}")
            return None

    def buscar_contactos_por_texto(self, texto):
        """
        Busca contactos que contengan un texto en su nombre, teléfono o correo.
        
        Parámetros:
        texto: palabra o frase que queremos buscar.
        
        Qué devuelve:
        - Lista de contactos que coinciden con el texto.
        """
        try:
            texto = texto.lower()  # Convierte el texto a minúsculas para búsqueda sin distinción de mayúsculas
            return [
                c for c in self.contactos
                if texto in c.nombre.lower() or texto in c.telefono.lower() or texto in c.correo.lower()
            ]
        except Exception as e:
            print(f"Error al buscar contactos: {e}")
            return []

    def listar_contactos(self):
        """
        Devuelve la lista completa de contactos.
        
        Útil para mostrar todos los contactos en pantalla.
        """
        return self.contactos

    # ---------------------- MÉTODOS DE FAVORITOS ----------------------
    def marcar_favorito(self, id_contacto):
        """
        Marca un contacto como favorito.
        
        Parámetros:
        id_contacto: ID del contacto que queremos marcar.
        
        Qué devuelve:
        - True si se pudo marcar.
        - False si el contacto no existe.
        """
        contacto = self.buscar_contacto_por_id(id_contacto)
        if contacto:
            contacto.marcar_favorito()  # Llama al método de Contacto para marcar como favorito
            self.guardar_contactos()
            return True
        return False

    def desmarcar_favorito(self, id_contacto):
        """
        Desmarca un contacto como favorito.
        
        Parámetros:
        id_contacto: ID del contacto que queremos desmarcar.
        
        Qué devuelve:
        - True si se pudo desmarcar.
        - False si el contacto no existe.
        """
        contacto = self.buscar_contacto_por_id(id_contacto)
        if contacto:
            contacto.desmarcar_favorito()  # Llama al método de Contacto para quitar el favorito
            self.guardar_contactos()
            return True
        return False
