import unittest
from modules.dominio import Usuario

class TestUsuario(unittest.TestCase):

    def test_creacion_valida(self):
        user = Usuario(1, "Juan","juan@mail.com", "1234","Pérez", "jperez", "Estudiante", "Usuario_final")
        self.assertEqual(user.nombre, "Juan")
        self.assertEqual(user.email, "juan@mail.com")
        self.assertEqual(user.rol, "Usuario_final")

    def test_email_invalido(self):
        with self.assertRaises(ValueError):
            Usuario(1, "Ana", "López", "correoSinArroba", "123", "analo", "Docente", "Usuario_final")

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Usuario(1, "   ", "García", "ana@mail.com", "123", "anagar", "Docente", "Usuario_final")

    def test_password_corta(self):
        with self.assertRaises(ValueError):
            Usuario(1, "Luis", "Suárez", "luis@mail.com", "12", "lsuarez", "Docente", "Usuario_final")

    def test_claustro_invalido(self):
        with self.assertRaises(ValueError):
            Usuario(1, "Marta", "Silva", "marta@mail.com", "123", "msilva", "Graduado", "Usuario_final")


if __name__ == '__main__':
    unittest.main()