# modules/utils.py
from flask import flash, redirect, url_for

def normalizar_departamento(departamento):
    """
    Normaliza el nombre de un departamento a un formato estándar.
    Parámetros:
        departamento (str): Nombre del departamento a normalizar.
    Retorna:
        str: Nombre normalizado del departamento si es reconocido.
    Acciones secundarias:
        Si el departamento no es reconocido, muestra un mensaje flash de error y redirige a la vista 'inicio'.
    Nota:
        Esta función depende de los métodos 'flash' y 'redirect' de Flask, así como de 'url_for'.
    """
    normalizaciones = {
        "maestranza": "Maestranza",
        "soporte informático": "Soporte_Informatico",
        "secretaría técnica": "Secretaria_Tecnica"
    }

    clave = departamento.lower()
    if clave not in normalizaciones:
        flash(f"Departamento no reconocido: '{departamento}'", 'danger')
        return redirect(url_for('inicio'))

    return normalizaciones[clave]