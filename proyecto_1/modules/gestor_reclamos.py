from modules.dominio import Reclamo
from modules.repositorio_abstracto import RepositorioAbstracto

class GestorDeReclamos:
    """
    Clase encargada de gestionar las operaciones relacionadas con los reclamos.
    Utiliza un repositorio que implementa la interfaz RepositorioAbstracto.
    """

    def __init__(self, repo: RepositorioAbstracto):
        """
        Inicializa el gestor con un repositorio dado y calcula el número de reclamos existentes.

        :param repo: Instancia de RepositorioAbstracto para acceder a los datos de reclamos.
        """
        self.__repo = repo    
        self.__numero_Reclamos = len(self.__repo.obtener_todos_los_registros())    

    @property
    def numero_Reclamos(self):
        """
        Retorna el número actual de reclamos registrados.

        :return: Cantidad de reclamos como entero.
        """
        return self.__numero_Reclamos

    def listar_Reclamos_existentes(self):
        """
        Lista todos los reclamos registrados en formato de diccionario.

        :return: Lista de reclamos (dict). Si no hay reclamos, retorna lista vacía.
        """
        registros = self.__repo.obtener_todos_los_registros()
        if not registros:
            return []
        return [Reclamo.to_dict() for Reclamo in registros]

    def agregar_nuevo_Reclamo(self, id_creador, estado, contenido, departamento, tiempo_en_proceso, r_imagen=None):
        """
        Crea y guarda un nuevo reclamo en el repositorio.

        :param id_creador: ID del usuario que crea el reclamo.
        :param estado: Estado inicial del reclamo (ej. "Pendiente").
        :param contenido: Descripción del reclamo.
        :param departamento: Departamento al que pertenece el reclamo.
        :param tiempo_en_proceso: Tiempo estimado de resolución.
        :param r_imagen: Ruta o nombre del archivo de imagen (opcional).
        """
        reclamo = Reclamo(id_reclamo=None, id_creador=id_creador,estado= estado,contenido= contenido,departamento= departamento,tiempo_en_proceso= tiempo_en_proceso,r_imagen= r_imagen)
        self.__repo.guardar_registro(reclamo)
        self.__numero_Reclamos += 1

    def devolver_Reclamo(self, id_Reclamo):         
        """
        Devuelve un reclamo a partir de su ID.

        :param id_Reclamo: ID del reclamo a buscar.
        :return: Instancia de Reclamo correspondiente.
        """
        return self.__repo.obtener_registro_por_filtro("id_reclamo", id_Reclamo)

    def editar_Reclamo(self, id_Reclamo, id_creador, estado, contenido, departamento, tiempo_en_proceso, r_imagen, fecha_y_hora):
        """
        Modifica un reclamo existente con los nuevos valores proporcionados.

        :param id_Reclamo: ID del reclamo a editar.
        :param id_creador: ID del autor del reclamo.
        :param estado: Nuevo estado del reclamo.
        :param contenido: Nuevo contenido o descripción del reclamo.
        :param departamento: Departamento asociado actualizado.
        :param tiempo_en_proceso: Tiempo estimado actualizado.
        :param r_imagen: ruta de la imagen del reclamo.
        :raises ValueError: Si el reclamo no existe.
        """
        if not isinstance(id_Reclamo, int) or id_Reclamo <= 0:
            raise ValueError("El ID del reclamo debe ser un entero positivo")
        if estado not in ["Pendiente", "En proceso", "Resuelto", "Invalido"] :
            raise ValueError("El estado del reclamo es erroneo. Debe ser uno de los siguientes: 'Pendiente', 'En proceso', 'Resuelto', 'Invalido'")
        if tiempo_en_proceso is not None: #Al crear un nuevo reclamo tiempo_en_proceso siempre es None, por eso es necesaria esta validación.
            if not isinstance(tiempo_en_proceso, int) or tiempo_en_proceso <= 0 or tiempo_en_proceso > 15:
                raise ValueError("El tiempo en proceso debe ser un entero entre 1 y 15 o None si aún no fue asignado")
        if self.__repo.obtener_registro_por_filtro("id_reclamo", id_Reclamo) is None:
            raise ValueError("El Reclamo no existe en la base de datos")

        reclamo = Reclamo(id_reclamo = id_Reclamo, id_creador = id_creador, estado = estado, contenido = contenido, departamento = departamento, tiempo_en_proceso = tiempo_en_proceso, r_imagen = r_imagen, fecha_y_hora = fecha_y_hora)
        self.__repo.modificar_registro(reclamo)

    def eliminar_Reclamo_seleccionado(self, id_Reclamo):  #Por el momento no se usa
        """
        Elimina un reclamo por su ID.

        :param id_Reclamo: ID del reclamo a eliminar.
        :raises ValueError: Si el reclamo no existe.
        """
        if self.__repo.obtener_registro_por_filtro("id_reclamo", id_Reclamo) is None:
            raise ValueError("El Reclamo no existe en la base de datos")
        self.__repo.eliminar_registro(id_Reclamo)
        self.__numero_Reclamos -= 1

    def devolver_reclamos_segun_usuario(self, id_creador):
        """
        Devuelve los reclamos asociados a un usuario (según el ID del creador del reclamo).

        :param id_creador: ID del usuario a buscar.
        :return: Lista con la representación en dict del reclamo encontrado.
        """
        reclamos = self.__repo.obtener_registros_por_filtro("id_creador", id_creador)
        if reclamos is None:
            reclamos = []
        return reclamos

    def obtener_reclamos_seguidos_por_usuario(self, id_usuario):
        """
        Devuelve todos los reclamos a los que un usuario está adherido.

        :param id_usuario: ID del usuario.
        :return: Lista de reclamos seguidos (como dict).
        """
        return [Reclamo.to_dict() for Reclamo in self.__repo.obtener_registros_adheridos_por_usuario(id_usuario)]

    def listar_reclamos_paginados(self, page=1, per_page=20, departamento=None):
        reclamos, total = self.__repo.obtener_reclamos_paginados(page, per_page, departamento)

        ids_reclamos = [r['id_reclamo'] for r in reclamos]
        adherentes_por_reclamo = self.__repo.contar_adherentes_por_varios_reclamos(ids_reclamos)

        for reclamo in reclamos:
            reclamo['n_adherentes'] = adherentes_por_reclamo.get(reclamo['id_reclamo'], 0)

        return reclamos, total


    def obtener_reclamos_departamento(self,departamento):
        reclamos = self.__repo.obtener_registros_por_filtro("departamento",departamento)
        return reclamos


