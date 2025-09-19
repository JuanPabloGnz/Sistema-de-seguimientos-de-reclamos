from abc import ABC, abstractmethod
@abstractmethod
class ExportadorReporte(ABC):
    """
    Clase base abstracta para exportadores de reportes.   
    """
    def generar_reporte(self, stats, departamento):
        """
        Método abstracto que debe ser implementado por las subclases para generar un reporte
        a partir de las estadísticas proporcionadas y el departamento especificado.
        Parámetros
        ----------
        stats : dict
            Diccionario que contiene las estadísticas a incluir en el reporte.
        departamento : str
            Nombre del departamento para el cual se genera el reporte.
        Raises
        ------
        NotImplementedError
        Si la subclase no implementa este método.
        """
        raise NotImplementedError