from modules.repositorio_concreto import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.config import crear_engine

def crear_repositorio():
    """
    Crea y devuelve instancias de los repositorios para reclamos y usuarios.

    Esta función inicializa una sesión de base de datos usando la función `crear_engine`
    y luego crea objetos repositorios concretos para reclamos y usuarios, vinculados
    a dicha sesión.

    :return: Una tupla (repo_reclamo, repo_usuario) con los repositorios instanciados.
    """
    session = crear_engine()
    repo_reclamo =  RepositorioReclamosSQLAlchemy(session())
    repo_usuario = RepositorioUsuariosSQLAlchemy(session())
    return repo_reclamo, repo_usuario