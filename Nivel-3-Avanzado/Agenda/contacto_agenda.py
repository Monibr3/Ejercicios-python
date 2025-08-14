import re  # Importamos el módulo 're' para usar expresiones regulares y validar correos

class Contacto:
    """
    Clase que representa un contacto de la agenda.
    
    Atributos:
    - id_contacto: identificador único del contacto
    - nombre: nombre del contacto
    - telefono: número de teléfono
    - direccion: dirección física
    - correo: dirección de correo electrónico (validada)
    - notas: información adicional opcional
    - favorito: indica si el contacto está marcado como favorito (True/False)
    """

    def __init__(self, id_contacto, nombre, telefono, direccion, correo, notas=""):
        """
        Constructor de la clase Contacto. Se ejecuta al crear un nuevo contacto.
        
        Parámetros:
        - id_contacto: ID único del contacto
        - nombre: nombre completo
        - telefono: número de teléfono
        - direccion: dirección física
        - correo: email (se valida)
        - notas: notas opcionales, por defecto cadena vacía
        
        Qué hace:
        1. Inicializa todos los atributos.
        2. Valida el correo electrónico usando 'validar_correo'.
        3. Si el correo es inválido, lanza un error (ValueError).
        """
        self.id_contacto = id_contacto
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.notas = notas
        self.favorito = False  # Por defecto, el contacto no es favorito

        # Validación del correo
        if self.validar_correo(correo):
            self.correo = correo
        else:
            # Lanza un error si el correo no tiene formato válido
            raise ValueError(f"Correo inválido: {correo}")

    def validar_correo(self, correo):
        """
        Valida que el correo tenga un formato básico correcto usando expresiones regulares.
        
        Parámetros:
        - correo: cadena de texto con el email a validar
        
        Devuelve:
        - True si el correo es válido
        - False si no cumple el patrón
        """
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Patrón básico: texto@texto.texto
        return re.match(patron, correo) is not None

    def to_dict(self):
        """
        Convierte el objeto Contacto en un diccionario para poder guardarlo en JSON.
        
        Devuelve un diccionario con todos los atributos.
        """
        return {
            "id_contacto": self.id_contacto,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "correo": self.correo,
            "notas": self.notas,
            "favorito": self.favorito
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea un objeto Contacto a partir de un diccionario (como los que se leen del JSON).
        
        Parámetros:
        - data: diccionario con los datos del contacto
        
        Devuelve:
        - Una instancia de Contacto con los datos cargados
        """
        contacto = cls(
            data["id_contacto"],
            data["nombre"],
            data["telefono"],
            data["direccion"],
            data["correo"],
            data.get("notas", "")  # Usa cadena vacía si no hay notas
        )
        contacto.favorito = data.get("favorito", False)  # Marca como favorito si el diccionario lo indica
        return contacto

    def mostrar_contacto(self):
        """
        Muestra los datos del contacto en pantalla de forma clara.
        """
        print(f"ID: {self.id_contacto}")
        print(f"Nombre: {self.nombre}")
        print(f"Teléfono: {self.telefono}")
        print(f"Dirección: {self.direccion}")
        print(f"Correo: {self.correo}")
        print(f"Notas: {self.notas}")
        print(f"Favorito: {'Sí' if self.favorito else 'No'}")  # Muestra 'Sí' si es favorito, 'No' si no lo es

    def marcar_favorito(self):
        """
        Marca este contacto como favorito.
        """
        self.favorito = True

    def desmarcar_favorito(self):
        """
        Desmarca este contacto como favorito.
        """
        self.favorito = False
