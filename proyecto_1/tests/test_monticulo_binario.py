from modules.monticulos import MonticuloBinario 
import unittest

class TestMonticuloBinario(unittest.TestCase):
    def test_insertar_en_monticulo_min(self):
        heap = MonticuloBinario("min")
        for val in [5, 3, 8, 1]:
            heap.insertar(val)
        # El mínimo debería estar en la raíz
        self.assertEqual(heap.listaMonticulo[1], 1)

    def test_insertar_en_monticulo_max(self):
        heap = MonticuloBinario("max")
        for val in [5, 3, 8, 1]:
            heap.insertar(val)
        # El máximo debería estar en la raíz
        self.assertEqual(heap.listaMonticulo[1], 8)

    def test_eliminar_en_monticulo_min(self):
        heap = MonticuloBinario("min")
        for val in [5, 3, 8, 1]:
            heap.insertar(val)
        eliminado = heap.eliminar()
        self.assertEqual(eliminado, 1)
        self.assertEqual(heap.tamanoActual, 3)

    def test_eliminar_en_monticulo_max(self):
        heap = MonticuloBinario("max")
        for val in [5, 3, 8, 1]:
            heap.insertar(val)
        eliminado = heap.eliminar()
        self.assertEqual(eliminado, 8)
        self.assertEqual(heap.tamanoActual, 3)

    def test_construir_monticulo_min(self):
        heap = MonticuloBinario("min")
        heap.construirMonticulo([4, 1, 3, 2])
        self.assertEqual(heap.listaMonticulo[1], 1)

    def test_construir_monticulo_max(self):
        heap = MonticuloBinario("max")
        heap.construirMonticulo([4, 1, 3, 2])
        self.assertEqual(heap.listaMonticulo[1], 4)

    def test_eliminar_hasta_vacio(self):
        heap = MonticuloBinario("min")
        datos = [7, 2, 6]
        for d in datos:
            heap.insertar(d)
        valores = [heap.eliminar() for _ in range(3)]
        self.assertEqual(sorted(valores), [2, 6, 7])
        self.assertEqual(heap.tamanoActual, 0)
    

if __name__ == '__main__':
    unittest.main()
