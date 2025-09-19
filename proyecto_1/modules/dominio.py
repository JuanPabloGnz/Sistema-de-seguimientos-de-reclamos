from datetime import datetime
from enum import Enum as enum


class Estado(enum):
    """
    Clase Estado
    Representa los posibles estados de un reclamo.
    Atributos:
        PENDIENTE (str): Estado inicial del reclamo.
        EN_PROCESO (str): Estado cuando el reclamo está siendo atendido.
        RESUELTO (str): Estado cuando el reclamo ha sido solucionado.
        INVALIDO (str): Estado cuando el reclamo es inválido o no procede.
    """
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTO = "Resuelto"
    INVALIDO = "Invalido"

class Reclamo:
    """
    Clase Reclamo
    Representa un reclamo realizado por un usuario en el sistema.
    Atributos:
        id_reclamo (int): Identificador único del reclamo.
        id_creador (int): Identificador del usuario que creó el reclamo.
        estado (str): Estado actual del reclamo. Puede ser "Pendiente", "En proceso", "Resuelto" o "Invalido".
        fecha_y_hora (datetime): Fecha y hora de creación del reclamo.
        contenido (str): Descripción o contenido del reclamo.
        departamento (str): Departamento al que pertenece el reclamo.
        tiempo_en_proceso (int): Tiempo que el reclamo lleva en proceso (en días).
        r_imagen (str): Ruta de la imagen asociada al reclamo (opcional).
    Métodos:
        to_dict(): Devuelve un diccionario con los datos del reclamo, formateando la fecha y hora como string.
    Propiedades:
        id_reclamo: Getter y setter para el identificador del reclamo.
        id_creador: Getter y setter para el identificador del creador.
        estado: Getter y setter para el estado del reclamo.
        fecha_y_hora: Getter y setter para la fecha y hora del reclamo.
        contenido: Getter y setter para el contenido del reclamo.
        departamento: Getter y setter para el departamento.
        tiempo_en_proceso: Getter y setter para el tiempo en proceso.
        r_imagen: Getter y setter para la ruta de la imagen.
    Excepciones:
        ValueError: Si alguno de los valores asignados a los atributos no cumple con las validaciones correspondientes.
    """
    def __init__(self,id_reclamo,id_creador,estado,contenido,departamento,r_imagen=None,fecha_y_hora=None, tiempo_en_proceso=None):
        '''Inicializa un nuevo reclamo con los parámetros proporcionados.'''
        self.id_reclamo = id_reclamo
        self.id_creador = id_creador
        self.estado = estado if estado is not None else "Pendiente" 
        self.fecha_y_hora = fecha_y_hora if fecha_y_hora is not None else datetime.now()
        self.contenido = contenido   
        self.departamento = departamento
        self.tiempo_en_proceso = tiempo_en_proceso
        self.r_imagen = r_imagen
         # --- GETTERS ---
    @property
    def id_reclamo(self):
        return self.__id_reclamo

    @property
    def id_creador(self):
        return self.__id_creador

    @property
    def estado(self):
        return self.__estado
    
    @property
    def fecha_y_hora(self):
        return self.__fecha_y_hora

    @property
    def contenido(self):
        return self.__contenido

    @property
    def departamento(self):
        return self.__departamento

    @property
    def tiempo_en_proceso(self):
        return self.__tiempo_en_proceso
    
    @property
    def r_imagen(self):
        return self.__r_imagen
    
    # --- SETTERS ---
    @id_reclamo.setter
    def id_reclamo(self, id_reclamo):
        if id_reclamo != None:
            if not isinstance(id_reclamo, int):
                raise ValueError("El id del reclamo debe ser un número entero")
            self.__id_reclamo = id_reclamo
        else:
            self.__id_reclamo = None

    @id_creador.setter
    def id_creador(self, id_creador):
        if id_creador != None:
            if not isinstance(id_creador, int):
                raise ValueError("El id del creador debe ser un número entero")
            self.__id_creador = id_creador
        else:
            self.__id_creador = None

    @estado.setter
    def estado(self, estado):
        estados_validos = ["Pendiente", "En proceso", "Resuelto", "Invalido"]
        if estado not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}.")
        self.__estado = estado

    @fecha_y_hora.setter
    def fecha_y_hora(self, fecha_y_hora):
        if not isinstance(fecha_y_hora, datetime):
            raise ValueError("La fecha y hora debe ser un objeto datetime.")
        self.__fecha_y_hora = fecha_y_hora

    @contenido.setter
    def contenido(self, contenido):
        if not isinstance(contenido, str) or not contenido.strip():
            raise ValueError("El contenido del reclamo no puede estar vacío.")
        self.__contenido = contenido.strip()

    @departamento.setter # Esto tiene que ser de tipo Departamento en vez de str
    def departamento(self, departamento):
        if not isinstance(departamento, str) or not departamento.strip():
            raise ValueError("El departamento no puede estar vacío.")
        self.__departamento = departamento.strip().title()

    @tiempo_en_proceso.setter
    def tiempo_en_proceso(self, tiempo_en_proceso):
        if tiempo_en_proceso is not None:
            if not isinstance(tiempo_en_proceso, int):
                raise ValueError("El tiempo a definir debe ser un entero y está medido en días.")
            if tiempo_en_proceso <= 0 or tiempo_en_proceso > 15:
                raise ValueError("El valor del tiempo en proceso no puede ser menor a 0 ni mayor a 15 días")
        self.__tiempo_en_proceso = tiempo_en_proceso

    @r_imagen.setter
    def r_imagen(self, valor):
        if valor is None:
            self.__r_imagen = None
        elif isinstance(valor, str):
            # Podés agregar validaciones aquí, por ejemplo que sea una ruta válida
            self.__r_imagen = valor
        else:
            raise ValueError(f"r_imagen debe ser una cadena o None, se recibió {type(valor).__name__}")

    def to_dict(self):
        '''Devuelve un diccionario con los datos del reclamo, formateando la fecha y hora como string.'''
        return {
            "id_reclamo":self.id_reclamo,
            "id_creador": self.id_creador,
            "estado": self.estado,
            "fecha_y_hora":self.fecha_y_hora.strftime("%d-%m-%Y %H:%M:%S"),
            "departamento":self.departamento,
            "contenido": self.contenido,
            "tiempo_en_proceso":self.tiempo_en_proceso,
            "r_imagen":self.r_imagen
            
        }
    
class Usuario:
    """
    Clase Usuario
    Representa un usuario del sistema con atributos personales y de acceso.
    Atributos:
        id (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        apellido (str): Apellido del usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
        nombre_usuario (str): Nombre de usuario para autenticación.
        claustro (str): Claustro al que pertenece el usuario ("Estudiante", "Docente", "PAyS").
        rol (str): Rol asignado al usuario.
    Métodos:
        __init__(self, id, nombre, email, password, apellido, nombre_usuario, claustro, rol):
            Inicializa una nueva instancia de Usuario con los datos proporcionados.
        to_dict(self):
            Devuelve un diccionario con los atributos del usuario.
    Excepciones:
        ValueError: Si alguno de los valores asignados no cumple con las validaciones correspondientes.
    """
    
    def __init__(self,id,nombre,email,password,apellido,nombre_usuario,claustro, rol):
        '''Inicializa un nuevo usuario con los parámetros proporcionados.'''
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.claustro = claustro
        self.rol = rol 

    # Getters    
    @property
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def apellido(self):
        return self.__apellido
    
    @property
    def email(self):
        return self.__email
    
    @property
    def nombre_usuario(self):
        return self.__nombre_usuario
    
    @property
    def password(self):
        return self.__password
    
    
    @property
    def claustro(self):
        return self.__claustro
    
    
    @property
    def rol(self):
        return self.__rol
    
    ## Setters
    @id.setter
    def id(self, id):
        if id != None:
            if not isinstance(id, int):
                raise ValueError("El id del usuario debe ser un número entero")
            self.__id = id
        else:
            self.__id = None
    

    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        self.__nombre = nombre.strip()

    @apellido.setter
    def apellido(self, apellido):
        if not isinstance(apellido, str) or not apellido.strip():
            raise ValueError("El apellido debe ser un texto no vacío.")
        self.__apellido = apellido.strip()

    @email.setter
    def email(self, email):
        self.__email = email.strip()
        if not isinstance(email, str) or "@" not in email or "." not in email:
            raise ValueError("El email debe ser una dirección válida.")
        
    @nombre_usuario.setter
    def nombre_usuario(self, nombre_usuario):
        if not isinstance(nombre_usuario, str) or not nombre_usuario.strip():
            raise ValueError("El nombre de usuario no puede estar vacío.")
        self.__nombre_usuario = nombre_usuario.strip()

    @claustro.setter
    def claustro(self, claustro):
        if claustro not in ["Estudiante", "Docente", "PAyS"]:
            raise ValueError("El claustro debe ser uno de: Estudiante, Docente, No docente, Graduado.")
        self.__claustro = claustro

    @password.setter
    def password(self, password):
        if not isinstance(password, str) or len(password) < 3:
            raise ValueError("La password debe tener al menos 3 caracteres.")
        self.__password = password

    @rol.setter
    def rol(self, rol):
        self.__rol = rol

    def to_dict(self):
        '''Devuelve un diccionario con los atributos del usuario.'''
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "nombre_usuario":self.nombre_usuario,
            "claustro":self.claustro,
            "rol":self.rol,
            "password": self.password

        }


