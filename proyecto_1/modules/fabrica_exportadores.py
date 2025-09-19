from modules.exportadores import ExportadorPDF, ExportadorHTML
def obtener_exportador(formato: str):
    """
    Devuelve una instancia del exportador correspondiente según el formato especificado.
    Parámetros:
        formato (str): El formato de exportación deseado.
    Retorna:
        Una instancia de la clase exportadora correspondiente al formato.
    Ejemplo:
        exportador = obtener_exportador('pdf')
    Nota:
        Las clases ExportadorFORMATO deben estar definidas previamente.
    """
    if formato == 'pdf':
        return ExportadorPDF()
    elif formato == 'html':
        return ExportadorHTML()
  # elif... para seguir agregando exportadores con otro formato
