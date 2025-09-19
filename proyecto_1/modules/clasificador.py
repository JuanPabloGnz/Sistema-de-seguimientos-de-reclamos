import pickle

class Clasificador:

    def __init__(self):
        """
        Inicializa la clase cargando un modelo de clasificación previamente entrenado.
        """
        with open('./data/claims_clf.pkl', 'rb') as archivo:
            self.clf = pickle.load(archivo)

    def clasificar(self, reclamos: list):
        """
        Clasifica una lista de reclamos utilizando un modelo previamente entrenado.
        Args:
            reclamos (list): Lista de textos de reclamos a clasificar.
        Returns:
            list: Lista de etiquetas predichas para cada reclamo.
        """
        return self.clf.predict(reclamos)

  