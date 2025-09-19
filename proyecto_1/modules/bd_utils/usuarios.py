from modules.gestor_usuarios import GestorDeUsuarios
from modules.gestor_reclamos import GestorDeReclamos
from modules.factoria import crear_repositorio
from modules.modelos import ModeloUsuario
from sqlalchemy import create_engine, update, text
from sqlalchemy.orm import sessionmaker

repo_reclamo, repo_usuario = crear_repositorio()
gestor_reclamos = GestorDeReclamos(repo_reclamo)
gestor_usuarios = GestorDeUsuarios(repo_usuario)

# def insertar_usuarios_jefes(jefes):
#     """
#     Inserta usuarios jefes en el sistema si no existen previamente.
#     Parámetros:
#         jefes (list of dict): Lista de diccionarios, cada uno representando un jefe con los siguientes campos:
#             - nombre (str): Nombre del jefe.
#             - apellido (str): Apellido del jefe.
#             - nombre_usuario (str): Nombre de usuario.
#             - email (str): Correo electrónico del jefe.
#             - password (str): Contraseña del jefe.
#             - claustro (str): Claustro al que pertenece (por ejemplo, 'Docente' o 'PAyS').
#             - rol (str): Rol del jefe (por ejemplo, 'Jefe_Maestranza', 'Jefe_Secretaria_Tecnica', 'Jefe_Soporte_Informatico').
#     Comportamiento:
#         Para cada jefe en la lista, verifica si el usuario ya existe autenticando con el email y la contraseña.
#         Si el usuario no existe, lo registra utilizando el gestor de usuarios.
#         Imprime un mensaje indicando si el usuario fue creado o si ya existía.
#     """     
#     for jefe in jefes:
#         try: 
#             gestor_usuarios.autenticar_usuario(jefe["email"], jefe["password"])
#             print(f"[SKIP] El usuario {jefe['email']} ya existe.")
#         except ValueError as e:
#             gestor_usuarios.registrar_nuevo_usuario(
#             nombre=jefe["nombre"],
#             apellido=jefe["apellido"],
#             nombre_usuario=jefe["nombre_usuario"],
#             email=jefe["email"],
#             password=jefe["password"],
#             claustro=jefe["claustro"],  
#             rol=jefe["rol"]
#         )
#             print(f"[OK] Usuario {jefe['email']} creado.")
        

    

if __name__ == "__main__":
    # jefes = [{"nombre": "Mariano", 
    #         "apellido": "Vazquez", 
    #         "nombre_usuario": "Mariv1", 
    #         "email": "mar@gmail.com", 
    #         "password": "12345", 
    #         "claustro": "Docente",
    #         "rol": "Jefe_Soporte_Informatico"},
    #         {"nombre": "Jorge", 
    #         "apellido": "Medici", 
    #         "nombre_usuario": "JorM1", 
    #         "email": "jorge@gmail.com", 
    #         "password": "12345", 
    #         "claustro": "PAyS",
    #         "rol": "Jefe_Soporte_Informatico"}]

    # insertar_usuarios_jefes(jefes)

    engine=create_engine('sqlite:///data/base_datos.db')
    Session = sessionmaker(bind=engine)
    session = Session()

  
    session.execute(
        update(ModeloUsuario)
        .where(ModeloUsuario.rol=='Usuario_final')
        .values(rol='Usuario_Final')
    )


    session.commit()
    session.close()


