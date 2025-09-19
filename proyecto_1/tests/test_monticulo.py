import unittest
from modules.monticulos import MonticuloMediana

class TestMonticuloMediana(unittest.TestCase):

    def setUp(self):
        self.monticulo = MonticuloMediana()

    def test_construccion_monticulo_valores_positivos(self):
        lista = [7, 1, 5, 2, 6, 8]
        self.monticulo.construir_monticulo(lista)
        self.assertAlmostEqual(self.monticulo.mediana, 5.5)

    def test_construccion_monticulo_valores_ordenados(self):
        lista = [1, 2, 3, 4, 5]
        self.monticulo.construir_monticulo(lista)
        self.assertEqual(self.monticulo.mediana, 3)

    def test_construccion_monticulo_valores_reversos(self):
        lista = [9, 8, 7, 6, 5]
        self.monticulo.construir_monticulo(lista)
        self.assertEqual(self.monticulo.mediana, 7)

    def test_construccion_monticulo_lista_vacia(self):
        self.monticulo.construir_monticulo([])
        self.assertIsNone(self.monticulo.mediana)

    def test_construccion_monticulo_con_negativos(self):
        lista = [3, -1, 4]
        self.monticulo.construir_monticulo(lista)
        self.assertEqual(self.monticulo.mediana, 3)

    def test_agregar_valor_aumenta_tamaño_total(self):
        self.monticulo.construir_monticulo([1, 2, 3])
        tamaño_antes = self.monticulo.devolver_tamaño()
        self.monticulo.agregar_valor(4)
        tamaño_despues = self.monticulo.devolver_tamaño()
        self.assertEqual(tamaño_despues, tamaño_antes + 1)

    def test_mediana_actualizada_correctamente(self):
        lista = [10, 20, 30, 40, 50]
        self.monticulo.construir_monticulo(lista)
        self.assertEqual(self.monticulo.mediana, 30)
        self.monticulo.agregar_valor(60)
        self.monticulo._MonticuloMediana__definir_mediana()
        self.assertEqual(self.monticulo.mediana, 35.0)

    def test_devolver_tamaño_correcto(self):
        self.monticulo.construir_monticulo([1, 2, 3, 4])
        self.assertEqual(self.monticulo.devolver_tamaño(), 4)

if __name__ == '__main__':
    unittest.main()
