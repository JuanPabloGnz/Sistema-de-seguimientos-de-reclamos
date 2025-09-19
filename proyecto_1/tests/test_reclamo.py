import unittest
from modules.dominio import Reclamo , Usuario
from datetime import datetime

class TestReclamo(unittest.TestCase):

    def test_creacion_valida(self):
        reclamo = Reclamo(id_reclamo=1,id_creador= 10,estado= "Pendiente",contenido= "Falta limpieza",departamento= "Maestranza",tiempo_en_proceso= 5,r_imagen= None)
        self.assertEqual(reclamo.id_reclamo, 1)
        self.assertEqual(reclamo.estado, "Pendiente")
        self.assertEqual(reclamo.departamento, "Maestranza")
        self.assertEqual(reclamo.tiempo_en_proceso, 5)

    def test_id_invalido(self):
        with self.assertRaises(ValueError):
            Reclamo("a", 1, "Pendiente", "Desc", "Depto", None, None, None)

    def test_estado_invalido(self):
        with self.assertRaises(ValueError):
            Reclamo(1, 1, "Finalizado", "Desc", "Depto", None, None, None)

    def test_contenido_vacio(self):
        with self.assertRaises(ValueError):
            Reclamo(1, 1, "Pendiente", "   ", "Depto", None, None, None)

    def test_departamento_vacio(self):
        with self.assertRaises(ValueError):
            Reclamo(1, 1, "Pendiente", "Desc", " ", None, 3, None)


if __name__ == '__main__':
    unittest.main()
