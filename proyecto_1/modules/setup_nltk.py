#Este archivo tiene el fin de dar solución a un problema de versiones en la libreria nltk.
#nltk es utilizada en el clasificador de reclamos, y a partir de la versión 3.8.2 en adelante,
#lanza un error porque no encuentra la carpeta punkt_tab. En versiones anteriores esta carpeta se llamaba punkt.
#Es necesario que se corra este código en el server.
#Link a foro de discusión sobre el tema: https://github.com/nltk/nltk/issues/3293
import nltk

class prechequeo_nltk():
    def asegurar_recursos_nltk():
        """
        Asegura que los recursos necesarios de NLTK estén disponibles.
        Verifica la presencia de los recursos 'punkt', 'punkt_tab' y 'stopwords' en la instalación local de NLTK.
        Si alguno de estos recursos no está disponible, lo descarga automáticamente utilizando nltk.download.
        No recibe parámetros ni retorna valores.
        Raises:
            Puede imprimir mensajes en consola si descarga recursos faltantes.
        """

        recursos = ["punkt", "punkt_tab", "stopwords"]
        for recurso in recursos:
            try:
                if recurso == "stopwords":
                    nltk.data.find("corpora/stopwords")
                else:
                    nltk.data.find(f"tokenizers/{recurso}")
            except LookupError:
                print(f"Descargando recurso NLTK: {recurso}")
                nltk.download(recurso)

if __name__ == "__main__":
    prechequeo_nltk.asegurar_recursos_nltk()