from modules.repositorio_abstracto import RepositorioAbstracto
from modules.monticulos import MonticuloMediana
from modules.graficador import Graficador
from modules.fabrica_exportadores import obtener_exportador
from collections import Counter

class Analitica():
    '''
    Clase Analitica para generar estadísticas y visualizaciones sobre reclamos de un departamento.
    Utiliza un repositorio que implementa la interfaz RepositorioAbstracto para acceder a los datos.'''
    def __init__(self, repo: RepositorioAbstracto):
        """
        Inicializa la clase con un repositorio dado.
        Args:
            repo (RepositorioAbstracto): Instancia de un repositorio que implementa la interfaz RepositorioAbstracto.
        """
        self.__repo = repo

    def generar_estadisticas(self, departamento):
        """
        Genera estadísticas y gráficos basados en los reclamos de un departamento específico.
        Parámetros:
            departamento (str): Nombre del departamento para filtrar los reclamos.
        Retorna:
            dict: Un diccionario con las siguientes claves:
                - "total" (int): Cantidad total de reclamos encontrados.
                - "porcentajes" (dict): Porcentaje de reclamos por estado.
                - "mediana_proceso" (float or None): Mediana del tiempo en proceso de los reclamos en estado "En proceso".
                - "mediana_resueltos" (float or None): Mediana del tiempo en proceso de los reclamos en estado "Resuelto".
                - "ruta_nube" (str or None): Ruta al archivo generado del gráfico de nube de palabras.
                - "ruta_torta" (str or None): Ruta al archivo generado del gráfico de torta de porcentajes por estado.
        Excepciones:
            Maneja internamente errores al calcular medianas y al generar gráficos, retornando None en caso de fallo.
        """
        lista_reclamos = self.__repo.obtener_registros_por_filtro("departamento", departamento)

        total = len(lista_reclamos)
        if total == 0:
            return {
                "total": 0,
                "porcentajes": {},
                "mediana_proceso": None,
                "mediana_resueltos": None,
                "ruta_nube": None,
                "ruta_torta": None
            }

        estados = [r.estado for r in lista_reclamos]
        tiempos_proceso = [r.tiempo_en_proceso for r in lista_reclamos if r.estado == "En proceso"]
        tiempos_resueltos = [r.tiempo_en_proceso for r in lista_reclamos if r.estado == "Resuelto"]

        conteo = Counter(estados)
        porcentajes = {estado: (conteo[estado] / total) * 100 for estado in conteo}

       # Mediana tiempos - con control de errores
        mediana_proceso = None
        mediana_resueltos = None

        try:
            if tiempos_proceso:  # Verificamos que haya datos
                monticulo_proceso = MonticuloMediana()
                monticulo_proceso.construir_monticulo(tiempos_proceso)
                mediana_proceso = monticulo_proceso.mediana
        except Exception as e:
            print(f"Error al calcular la mediana de tiempos en proceso: {e}")
            mediana_proceso = None

        try:
            if tiempos_resueltos:  # Verificamos que haya datos
                monticulo_resueltos = MonticuloMediana()
                monticulo_resueltos.construir_monticulo(tiempos_resueltos)
                mediana_resueltos = monticulo_resueltos.mediana
        except Exception as e:
            print(f"Error al calcular la mediana de tiempos resueltos: {e}")
            mediana_resueltos = None

        # Grafico de nube
        textos = " ".join([r.contenido.lower() for r in lista_reclamos])
        output_file_nube = Graficador.graficar_nube(textos)

        # Grafico de torta
        output_file_torta = Graficador.graficar_torta(porcentajes)    


        return {
            "total": total,
            "porcentajes": porcentajes,
            "mediana_proceso": mediana_proceso,
            "mediana_resueltos": mediana_resueltos,
            "ruta_nube": output_file_nube,
            "ruta_torta": output_file_torta
        }
    
    def exportar_archivo(self, departamento: str, formato: str):
        stats = self.generar_estadisticas(departamento)
        exportador = obtener_exportador(formato)
        return exportador.generar_reporte(stats, departamento)
    
    