from modules.dominio import Usuario
from modules.repositorio_abstracto import RepositorioAbstracto
from werkzeug.security import generate_password_hash, check_password_hash


class GestorDeUsuarios:
    '''Clase encargada de gestionar las operaciones relacionadas con los usuarios.
    Utiliza un repositorio que implementa la interfaz RepositorioAbstracto para acceder a los datos.'''
    def __init__(self, repo: RepositorioAbstracto):
        '''Inicializa el gestor con un repositorio dado.'''
        self.__repo = repo

    def registrar_nuevo_usuario(self, nombre, email, password, apellido, nombre_usuario, claustro, rol):
        """
        Registra un nuevo usuario en el sistema.
        Verifica si el email proporcionado ya está registrado. Si es así, lanza una excepción.
        Si no, encripta la contraseña, crea una instancia de Usuario y la guarda en el repositorio.
        Args:
            nombre (str): Nombre del usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña en texto plano del usuario.
            apellido (str): Apellido del usuario.
            nombre_usuario (str): Nombre de usuario.
            claustro (str): Claustro al que pertenece el usuario.
            rol (str): Rol asignado al usuario.
        Raises:
            ValueError: Si el email ya está registrado en el sistema.
        """
        if self.__repo.obtener_registro_por_filtro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        pass_encriptada = generate_password_hash(password= password,
                                                 method= 'pbkdf2:sha256',
                                                 salt_length=8
                                                )
        usuario = Usuario(None, nombre, email, pass_encriptada, apellido, nombre_usuario, claustro, rol)
        self.__repo.guardar_registro(usuario)

    def autenticar_usuario(self, email, password):
        """
        Autentica a un usuario verificando su correo electrónico y contraseña.
        Args:
            email (str): Correo electrónico del usuario a autenticar.
            password (str): Contraseña proporcionada para la autenticación.
        Returns:
            Usuario: Objeto de usuario autenticado si las credenciales son correctas.
        Raises:
            ValueError: Si el usuario no está registrado o la contraseña es incorrecta.
        """
        usuario = self.__repo.obtener_registro_por_filtro("email", email)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        elif not check_password_hash(usuario.password, password):
            raise ValueError("Contraseña incorrecta")
        return usuario
        
    def cargar_usuario(self, id_usuario):
        """
        Carga y devuelve la información de un usuario específico según su ID.
        Args:
            id_usuario (int or str): El identificador único del usuario a buscar.
        Returns:
            dict: Un diccionario con los datos del usuario correspondiente al ID proporcionado.
        """
        return self.__repo.obtener_registro_por_filtro("id", id_usuario).to_dict()
    
    def registrar_reclamo_a_seguir(self, id_usuario, id_reclamo):
        """
        Registra que un usuario desea seguir (adherirse a) un reclamo específico.
        Args:
            id_usuario (int): El identificador único del usuario que desea adherirse al reclamo.
            id_reclamo (int): El identificador único del reclamo al que el usuario desea adherirse.
        Raises:
            ValueError: Si el usuario no está registrado.
            ValueError: Si el usuario ya está adherido al reclamo.
        """

        usuario = self.__repo.obtener_registro_por_filtro("id", id_usuario)
        if not usuario:
            raise ValueError("El usuario no está registrado")

        adherentes = self.__repo.obtener_adherentes_de_registro_asociado(id_reclamo)
        if any(usuario.id == id_usuario for usuario in adherentes):
            raise ValueError("Usted ya se encuentra adherido al reclamo")

        self.__repo.asociar_registro(id_usuario, id_reclamo)

    def contar_adherentes_de_reclamo(self, id_Reclamo):
        """
        Cuenta la cantidad de adherentes asociados a un reclamo específico.
        Args:
            id_Reclamo (int): El identificador único del reclamo.
        Returns:
            int: La cantidad de adherentes asociados al reclamo.
        """
        adherentes = self.__repo.obtener_adherentes_de_registro_asociado(id_Reclamo)
        return len(adherentes)