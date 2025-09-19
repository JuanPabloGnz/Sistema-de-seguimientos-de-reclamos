from modules.dominio import Reclamo, Usuario
from modules.modelos import ModeloReclamo, ModeloUsuario, asociacion_usuarios_reclamos
from modules.repositorio_abstracto import RepositorioAbstracto
from sqlalchemy import func

class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    """
    Repositorio de acceso a datos para usuarios, implementado con SQLAlchemy.
    Permite operaciones CRUD y la asociación con reclamos.
    """

    def __init__(self, session):
        """
        Inicializa el repositorio con una sesión de base de datos SQLAlchemy.

        :param session: Objeto de sesión de SQLAlchemy.
        """
        self.__session = session
        tabla_usuario = ModeloUsuario()
        tabla_usuario.metadata.create_all(self.__session.bind)

    def guardar_registro(self, entidad):
        """
        Guarda un nuevo usuario en la base de datos.

        :param entidad: Instancia de Usuario.
        :raises ValueError: Si el objeto no es instancia de Usuario.
        """
        if not isinstance(entidad, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        modelo_usuario = self.__map_entidad_a_modelo(entidad)
        self.__session.add(modelo_usuario)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        """
        Obtiene todos los usuarios de la base de datos.

        :return: Lista de objetos Usuario.
        """
        modelo_usuarios = self.__session.query(ModeloUsuario).all()
        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_usuarios]

    def modificar_registro(self, entidad_modificada):
        """
        Modifica un usuario existente en la base de datos.

        :param entidad_modificada: Instancia de Usuario con datos nuevos.
        :raises ValueError: Si el objeto no es instancia de Usuario.
        """
        if not isinstance(entidad_modificada, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        register = self.__session.query(ModeloUsuario).filter_by(id=entidad_modificada.id).first()
        register.nombre = entidad_modificada.nombre
        register.apellido = entidad_modificada.apellido
        register.email = entidad_modificada.email
        register.password = entidad_modificada.password
        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        """
        Obtiene un usuario según un filtro.

        :param filtro: Nombre del campo.
        :param valor: Valor a buscar.
        :return: Usuario si se encuentra, None si no.
        """
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(**{filtro: valor}).first()
        return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None

    def asociar_registro(self, id, id_asociado):
        """
        Asocia un usuario a un reclamo (adherirse a un reclamo).

        :param id: ID del usuario.
        :param id_asociado: ID del reclamo.
        """
        register = self.__session.query(ModeloUsuario).filter_by(id=id).first()
        modelo_reclamo = self.__session.query(ModeloReclamo).filter_by(id_reclamo=id_asociado).first()
        register.reclamos_adheridos.append(modelo_reclamo)
        self.__session.commit()

    def obtener_adherentes_de_registro_asociado(self, id_asociado):
        """
        Obtiene todos los usuarios que se adhirieron a un reclamo.

        :param id_asociado: ID del reclamo.
        :return: Lista de usuarios adherentes.
        """
        modelo_reclamo = self.__session.query(ModeloReclamo).filter_by(id_reclamo=id_asociado).first()
        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_reclamo.usuarios_adherentes]

    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
        """
        Convierte un modelo de SQLAlchemy a una entidad Usuario.

        :param modelo: ModeloUsuario.
        :return: Usuario.
        """
        return Usuario(
            modelo.id,
            modelo.nombre,
            modelo.email,
            modelo.password,
            modelo.apellido,
            modelo.nombre_usuario,
            modelo.claustro,
            modelo.rol
        )

    def __map_entidad_a_modelo(self, entidad):
        """
        Convierte una entidad Usuario a un modelo SQLAlchemy.

        :param entidad: Usuario.
        :return: ModeloUsuario.
        """
        return ModeloUsuario(
            nombre=entidad.nombre,
            email=entidad.email,
            password=entidad.password,
            apellido=entidad.apellido,
            nombre_usuario=entidad.nombre_usuario,
            claustro=entidad.claustro,
            rol=entidad.rol
        )


class RepositorioReclamosSQLAlchemy(RepositorioAbstracto):
    """
    Repositorio de acceso a datos para reclamos, implementado con SQLAlchemy.
    Gestiona operaciones CRUD y asociaciones con usuarios.
    """

    def __init__(self, session):
        """
        Inicializa el repositorio con una sesión de base de datos SQLAlchemy.

        :param session: Objeto de sesión SQLAlchemy.
        """
        self.__session = session
        tabla_reclamo = ModeloReclamo()
        tabla_reclamo.metadata.create_all(self.__session.bind)

    def guardar_registro(self, entidad):
        """
        Guarda un nuevo reclamo en la base de datos.

        :param entidad: Instancia de Reclamo.
        :raises ValueError: Si el objeto no es instancia de Reclamo.
        """
        if not isinstance(entidad, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        modelo_reclamo = self.__map_entidad_a_modelo(entidad)
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        """
        Obtiene todos los reclamos de la base de datos.

        :return: Lista de objetos Reclamo.
        """
        modelo_reclamos = self.__session.query(ModeloReclamo).all()
        return [self.__map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def modificar_registro(self, entidad_modificada):
        """
        Modifica un registro existente. Toma los atributos de la entidad_modificada y actualiza el registro 
        existente a partir de estos. No permite modificar id_reclamo ni id_creador.

        :param entidad_modificada: Instancia modificada de Reclamo.
        :raises ValueError: Si el reclamo no existe o el objeto no es válido.
        """
        if not isinstance(entidad_modificada, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        register = self.__session.query(ModeloReclamo).filter_by(id_reclamo=entidad_modificada.id_reclamo).first()
        if not register:
            raise ValueError("No se encontró el reclamo con ese id")
        register.estado = entidad_modificada.estado
        register.tiempo_en_proceso = entidad_modificada.tiempo_en_proceso
        register.departamento = entidad_modificada.departamento
        register.contenido = entidad_modificada.contenido
        register.r_imagen = entidad_modificada.r_imagen
        self.__session.flush()
        self.__session.commit()

    def obtener_registro_por_filtro(self, filtro, valor):
        """
        Busca un reclamo por un campo específico.

        :param filtro: Campo por el cual filtrar.
        :param valor: Valor a buscar.
        :return: Instancia de Reclamo.
        :raises ValueError: Si no se encuentra el reclamo.
        """
        modelo_reclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()
        if modelo_reclamo is None:
            raise ValueError("Reclamo no encontrado")
        return self.__map_modelo_a_entidad(modelo_reclamo)

    def obtener_registros_por_filtro(self, filtro, valor):
        """
        Obtiene múltiples reclamos según un filtro.

        :param filtro: Campo de filtro.
        :param valor: Valor a buscar.
        :return: Lista de Reclamo.
        """
        modelos_reclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).all()
        return [self.__map_modelo_a_entidad(m) for m in modelos_reclamo]

    def obtener_registros_adheridos_por_usuario(self, id_usuario):
        """
        Devuelve todos los reclamos a los que un usuario está adherido.

        :param id_usuario: ID del usuario.
        :return: Lista de Reclamo.
        """
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(id=id_usuario).first()
        return [self.__map_modelo_a_entidad(reclamo) for reclamo in modelo_usuario.reclamos_adheridos]
    
    def obtener_reclamos_paginados(self, page, per_page, departamento=None):
        offset = (page - 1) * per_page
        query = self.__session.query(ModeloReclamo)

        if departamento:
            query = query.filter_by(departamento=departamento)

        query = query.order_by(ModeloReclamo.id_reclamo.desc())

        total = query.count()
        resultados = query.limit(per_page).offset(offset).all()
        

        reclamos = [self.__map_modelo_a_entidad(m).to_dict() for m in resultados]
        return reclamos, total

    def contar_adherentes_por_varios_reclamos(self, lista_ids):
        
        resultados = (
            self.__session.query(
                asociacion_usuarios_reclamos.c.id_reclamo,
                func.count(asociacion_usuarios_reclamos.c.id_usuario).label('total')
            )
            .filter(asociacion_usuarios_reclamos.c.id_reclamo.in_(lista_ids))
            .group_by(asociacion_usuarios_reclamos.c.id_reclamo)
            .all()
        )
        return {id_reclamo: total for id_reclamo, total in resultados}

    def contar_total_reclamos(self):
        return self.__session.query(func.count(ModeloReclamo.id_reclamo)).scalar()

    def __map_modelo_a_entidad(self, modelo: ModeloReclamo):
        """
        Convierte un modelo SQLAlchemy a una entidad Reclamo.

        :param modelo: ModeloReclamo.
        :return: Reclamo.
        """
        return Reclamo(
            id_reclamo=modelo.id_reclamo,
            id_creador=modelo.id_creador,
            estado=modelo.estado,
            fecha_y_hora=modelo.fecha_y_hora,
            contenido=modelo.contenido,
            departamento=modelo.departamento,
            r_imagen=modelo.r_imagen,
            tiempo_en_proceso=modelo.tiempo_en_proceso,
        )

    def __map_entidad_a_modelo(self, entidad: Reclamo):
        """
        Convierte una entidad Reclamo a un modelo SQLAlchemy.

        :param entidad: Reclamo.
        :return: ModeloReclamo.
        """
        return ModeloReclamo(
            id_reclamo=entidad.id_reclamo,
            id_creador=entidad.id_creador,
            estado=entidad.estado,
            fecha_y_hora=entidad.fecha_y_hora,
            contenido=entidad.contenido,
            departamento=entidad.departamento,
            r_imagen=entidad.r_imagen,
            tiempo_en_proceso=entidad.tiempo_en_proceso
        )
