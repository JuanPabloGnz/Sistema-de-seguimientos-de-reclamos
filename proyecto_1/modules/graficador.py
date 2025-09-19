import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import string

# Lista local de palabras vacías en español (puedes ampliarla si querés)
STOPWORDS_ES = set([
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por",
    "un", "para", "con", "no", "una", "su", "al", "lo", "como", "más", "pero",
    "sus", "le", "ya", "o", "este", "sí", "porque", "esta", "entre", "cuando"
])

class Graficador():
    """
    Clase que proporciona métodos estáticos para generar gráficos:
    - Gráfico de torta (pie chart) a partir de porcentajes.
    - Nube de palabras a partir de textos, filtrando palabras vacías.
    """

    @staticmethod
    def graficar_torta(porcentajes, ruta_salida='static/images/torta.png'):
        """
        Genera y guarda un gráfico de torta (pie chart) con etiquetas y porcentajes.

        :param porcentajes: Diccionario con etiquetas como claves y valores numéricos (porcentajes).
        :param ruta_salida: Ruta donde se guardará la imagen generada (PNG).
        :return: Ruta donde se guardó la imagen.
        """
        labels = porcentajes.keys()
        sizes = porcentajes.values()
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(ruta_salida)
        return ruta_salida

    @staticmethod
    def graficar_nube(textos_contenidos, ruta_salida = 'static/images/nube.png'):
        """
        Genera y guarda una imagen de nube de palabras a partir de un texto.

        Elimina signos de puntuación y palabras vacías definidas en STOPWORDS_ES,
        luego genera la nube con las 15 palabras más frecuentes.

        :param textos_contenidos: Texto en formato string a procesar.
        :return: Ruta donde se guardó la imagen generada (PNG).
        """
        ruta_salida = 'static/images/nube.png'
        texto_limpio = textos_contenidos.translate(str.maketrans('', '', string.punctuation))
        palabras = texto_limpio.split()
        palabras_filtradas = [p for p in palabras if p not in STOPWORDS_ES]
        frecuencia = Counter(palabras_filtradas).most_common(15)
        texto_final = " ".join([(" " + palabra) * freq for palabra, freq in frecuencia])
        nube = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(texto_final)
        nube.to_file(ruta_salida)
        return ruta_salida


if __name__ == "__main__":
    
    porcentajes = {'resuelto' : 75,
                   'pendiente' : 10,
                   'en_proceso' : 5,
                   'invalido' : 10}
    
    Graficador.graficar_torta(porcentajes)
