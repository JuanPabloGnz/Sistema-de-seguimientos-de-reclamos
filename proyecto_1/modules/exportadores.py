from modules.exportador import ExportadorReporte
import os
import io
from io import BytesIO
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ExportadorPDF(ExportadorReporte):
    def generar_reporte(self, stats : dict, departamento):
        """
        Genera un reporte en formato PDF con estadísticas y gráficos para un departamento específico.
        Args:
            stats (dict): Diccionario con estadísticas del departamento, incluyendo:
                - 'total': Total de reclamos.
                - 'porcentajes': Distribución porcentual por estado.
                - 'mediana_proceso': Mediana del tiempo de resolución para reclamos en proceso.
                - 'mediana_resueltos': Mediana del tiempo de resolución para reclamos resueltos.
                - 'ruta_torta': Ruta al archivo de imagen del gráfico de torta (opcional).
                - 'ruta_nube': Ruta al archivo de imagen de la nube de palabras (opcional).
            departamento (str): Nombre o identificador del departamento.
        Returns:
            tuple: (buffer, mime_type, filename)
                - buffer (BytesIO): Buffer con el contenido del PDF generado.
                - mime_type (str): Tipo MIME del archivo ('application/pdf').
                - filename (str): Nombre sugerido para el archivo PDF.
        """

        buffer = BytesIO()

        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Reporte - Departamento {departamento}")

        y = height - 80
        c.setFont("Helvetica", 12)

        c.drawString(50, y, f"Total de Reclamos: {stats['total']}")
        y -= 25

        c.drawString(50, y, "Distribución por Estado:")
        y -= 20
        for estado, porcentaje in stats['porcentajes'].items():
            c.drawString(70, y, f"{estado}: {porcentaje:.2f}%")
            y -= 18

        y -= 10
        c.drawString(50, y, "Mediana del Tiempo de Resolución:")
        y -= 20
        c.drawString(70, y, f"En proceso: {stats['mediana_proceso'] or 'N/A'}")
        y -= 18
        c.drawString(70, y, f"Resueltos: {stats['mediana_resueltos'] or 'N/A'}")
        y -= 40

        if stats['ruta_torta'] and os.path.exists(stats['ruta_torta']):
            c.drawString(50, y, "Gráfico de Torta:")
            y -= 160
            c.drawImage(stats['ruta_torta'], 50, y, width=400, height=150, preserveAspectRatio=True)
            y -= 160

        if stats['ruta_nube'] and os.path.exists(stats['ruta_nube']):
            c.drawString(50, y, "Nube de Palabras:")
            y -= 160
            c.drawImage(stats['ruta_nube'], 50, y, width=400, height=150, preserveAspectRatio=True)
            y -= 160

        c.save()
        buffer.seek(0)
        return buffer, 'application/pdf', f'reporte_{departamento}.pdf'

class ExportadorHTML(ExportadorReporte):
    """
    Clase para exportar reportes en formato HTML, incluyendo estadísticas y gráficos embebidos en base64.
    Esta clase permite generar un archivo HTML que resume información estadística de reclamos para un departamento específico,
    incluyendo gráficos (como tortas y nubes de palabras) embebidos directamente en el HTML mediante codificación base64.
    Métodos:
        __imagen_a_base64(path):
            Convierte una imagen en la ruta especificada a una cadena base64 para embeber en HTML.
        generar_reporte(stats, departamento):
            Genera un reporte HTML con estadísticas y gráficos para el departamento dado, devolviendo un buffer listo para guardar o enviar.
    """
    #Este metodo es necesario para embeber las imagenes en el html
    def __imagen_a_base64(self, path):
        """
        Convierte un archivo de imagen a una cadena codificada en base64.
        Args:
            path (str): Ruta al archivo de imagen.
        Returns:
            str: Cadena codificada en base64 de la imagen.
        Raises:
            FileNotFoundError: Si el archivo no existe.
            IOError: Si el archivo no puede ser leído.
        """
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
            
    def generar_reporte(self, stats : dict, departamento):
        """           
        Genera un reporte HTML con estadísticas y gráficos para un departamento específico.
        Args:
            stats (dict): Diccionario con estadísticas y rutas de imágenes generadas. Debe contener las claves:
                - 'ruta_torta': Ruta al archivo de imagen del gráfico de torta.
                - 'ruta_nube': Ruta al archivo de imagen de la nube de palabras.
                - 'total': Total de reclamos.
                - 'porcentajes': Diccionario con porcentajes por estado.
                - 'mediana_proceso': Mediana de tiempos para reclamos en proceso.
                - 'mediana_resueltos': Mediana de tiempos para reclamos resueltos.
            departamento (str): Nombre del departamento para el cual se genera el reporte.
        Returns:
            tuple: (buffer_html, 'text/html', nombre_archivo)
                - buffer_html (io.BytesIO): Buffer con el contenido HTML codificado en UTF-8.
                - 'text/html': Tipo MIME del contenido.
                - nombre_archivo (str): Nombre sugerido para el archivo HTML generado.
        """
        if stats['ruta_torta'] and os.path.exists(stats['ruta_torta']):
            img_torta_base64 = self.__imagen_a_base64(stats['ruta_torta'])
        else:
            img_torta_base64 = ""

        if stats['ruta_nube'] and os.path.exists(stats['ruta_nube']):
            img_nube_base64 = self.__imagen_a_base64(stats['ruta_nube'])
        else:
            img_nube_base64 = ""

        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head><meta charset="UTF-8"><title>Reporte {departamento}</title></head>
        <body>
            <h1>Reporte del Departamento {departamento}</h1>
            <p><strong>Total de Reclamos:</strong> {stats['total']}</p>
            <h3>Distribución por Estado</h3>
            <ul>
                {''.join(f'<li>{estado}: {round(p, 2)}%</li>' for estado, p in stats['porcentajes'].items())}
            </ul>
            <h3>Mediana de Tiempos</h3>
            <p>En proceso: {stats['mediana_proceso'] or 'N/A'}</p>
            <p>Resueltos: {stats['mediana_resueltos'] or 'N/A'}</p>
            <h3>Gráficos</h3>
            {"<img src='data:image/png;base64," + img_torta_base64 + "' width='400'><br>" if img_torta_base64 else "<p>No se pudo generar la gráfica de torta</p>"}
            {"<img src='data:image/png;base64," + img_nube_base64 + "' width='400'>" if img_nube_base64 else "<p>No se pudo generar la nube de palabras</p>"}
        </body>
        </html>
        """
        buffer_html = io.BytesIO(html_content.encode('utf-8'))
        buffer_html.seek(0)
        return buffer_html, 'text/html', f'reporte_{departamento}.html'
    