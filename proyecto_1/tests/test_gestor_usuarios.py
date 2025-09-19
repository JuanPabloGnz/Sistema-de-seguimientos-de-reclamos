import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.modelos import ModeloUsuario, ModeloReclamo, Base
from modules.repositorio_concreto import RepositorioUsuariosSQLAlchemy 
from modules.gestor_usuarios import GestorDeUsuarios
from werkzeug.security import check_password_hash


class TestGestorDeUsuarios(unittest.TestCase):

    def setUp(self):
        # Base de datos en memoria
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Repositorio y gestor a testear
        self.repo = RepositorioUsuariosSQLAlchemy(self.session)
        self.gestor = GestorDeUsuarios(self.repo)

    def test_registrar_usuario_exitoso(self):
        self.gestor.registrar_nuevo_usuario("Ana", "ana@mail.com", "clave123", 
                                            "Perez", "anaperez", "Estudiante", "Usuario_final")
        usuario = self.repo.obtener_registro_por_filtro("email", "ana@mail.com")

        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.email, "ana@mail.com")
        self.assertTrue(check_password_hash(usuario.password, "clave123"))

    def test_registro_falla_si_email_ya_existe(self):
        self.gestor.registrar_nuevo_usuario("Ana", "ana@mail.com", "clave123", 
                                            "Perez", "anaperez", "Estudiante", "Usuario_final")
        with self.assertRaises(ValueError) as contexto:
            self.gestor.registrar_nuevo_usuario("Ana", "ana@mail.com", "clave123", 
                                                "Perez", "anaperez", "Estudiante", "Usuario_final")

        self.assertIn("ya está registrado", str(contexto.exception))

    def test_autenticar_usuario_correctamente(self):
        self.gestor.registrar_nuevo_usuario("Ana", "ana@mail.com", "clave123", 
                                            "Perez", "anaperez", "Estudiante", "Usuario_final")
        usuario = self.gestor.autenticar_usuario("ana@mail.com", "clave123")
        self.assertEqual(usuario.nombre, "Ana")


    def test_autenticar_usuario_contraseña_incorrecta(self):
        self.gestor.registrar_nuevo_usuario("Ana", "ana@mail.com", "clave123", 
                                            "Perez", "anaperez", "Estudiante", "Usuario_final")
        with self.assertRaises(ValueError) as contexto:
            self.gestor.autenticar_usuario("ana@mail.com", "mala")

        self.assertIn("Contraseña incorrecta", str(contexto.exception))

    def test_autenticar_usuario_no_existe(self):
        with self.assertRaises(ValueError) as contexto:
            self.gestor.autenticar_usuario("nadie@mail.com", "clave")

        self.assertIn("no está registrado", str(contexto.exception))

    def test_cargar_usuario_por_id(self):
        self.gestor.registrar_nuevo_usuario("Ana", "ana@mail.com", "clave123", 
                                            "Perez", "anaperez", "Estudiante", "Usuario_final")
        usuario = self.repo.obtener_registro_por_filtro("email", "ana@mail.com")
        usuario_dict = self.gestor.cargar_usuario(usuario.id)

        self.assertEqual(usuario_dict['email'], "ana@mail.com")

    def test_registrar_reclamo_a_seguir(self):
        # Crear usuario
        self.gestor.registrar_nuevo_usuario("Ana", "ana@mail.com", "clave123", 
                                            "Perez", "anaperez", "Estudiante", "Usuario_final")
        usuario = self.repo.obtener_registro_por_filtro("email", "ana@mail.com")

        # Crear reclamo manualmente
        reclamo = ModeloReclamo(id_reclamo=1, id_creador=usuario.id, contenido="algo", estado="Pendiente", departamento="Maestranza")
        self.session.add(reclamo)
        self.session.commit()

        # Asociar usuario al reclamo
        self.gestor.registrar_reclamo_a_seguir(usuario.id, 1)

        # Verificar la asociación
        adherentes = self.repo.obtener_adherentes_de_registro_asociado(1)
        self.assertEqual(len(adherentes), 1)
        self.assertEqual(adherentes[0].email, "ana@mail.com")
    




if __name__ == '__main__':
    unittest.main()
