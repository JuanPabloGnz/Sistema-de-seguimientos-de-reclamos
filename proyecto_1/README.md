# 🐍Sistema CRM de reclamos en una universidad 

Breve descripción del proyecto:

Esta es una aplicación web construida con el framework [Flask](https://flask.palletsprojects.com/). Permite el registro y seguimiento de reclamos para distintos departamentos de una universidad. 
---
## 🏗Arquitectura General

El sistema está dividido y organizado en distintas carpetas. A continuación se detalla el contenido de cada una de estas:

El diagrama de relaciones entre clases está disponible en la carpeta [docs](./docs) del proyecto.

Los Repositorios Concretos se encuentran en la carpeta [modules](./modules) en el archivo repositorio_concreto.py

Los gestores en la carpeta [modules](./modules) donde cada uno tiene dedicado un archivo especifico: gestor_login.py y gestor_usuarios.py

Tenemos Dominio y Factoria en la carpeta [modules](./modules)

Los modelos para la base de datos en la carpeta [modules](./modules) en el archivo modelos.py

Por ultimo modulos especificos como graficador.py y monticulos.py que se encuentran en la carpeta [modules](./modules) 

En la carpeta [templates](./templates) tenemos todas las paginas html a las que los usuarios irán accediendo en el sistema.

En la carpeta [data](./data) se almacena nuestra base de datos

Las pruebas unitarias se encuentran en [tests](./tests)



---
## 📑Dependencias

flask
flask_session
sqlalchemy
flask_login
flask_bootstrap
flask_wtf
email_validator
matplotlib
datetime
wordcloud
numpy
collections

---
## 🚀Cómo Ejecutar el Proyecto
1. **Clonar o descargar** el repositorio.

2. **Crear y activar** un entorno virtual.

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   El archivo `requirements.txt` se encuentran en la carpeta [deps](./deps) del proyecto.
---

## 💻Uso de la aplicación

Acceso y Perfiles de Usuario
Para comenzar, los usuarios deben iniciar sesión en el sistema. Si aún no tienen una cuenta, pueden registrarse completando el formulario de creación de cuenta. Una vez que hayan cargado su información, podrán iniciar sesión y acceder a la vista correspondiente a su rol asignado.

Funcionalidades por Rol
Según el rol del usuario, las funcionalidades disponibles varían:

Estudiante, Docente o Personal Administrativo (sin rol de Jefe de Departamento)
Los usuarios con estos roles pueden:

Crear nuevos reclamos.
Visualizar todos los reclamos existentes.
Ver sus propios reclamos registrados.
Adherirse a reclamos creados por otros usuarios.
Jefe de Departamento
Los Jefes de Departamento tienen acceso a un panel de control con las siguientes funciones:

Analíticas: Permite ver estadísticas y gráficos relacionados con los reclamos de su departamento.
Gestión de reclamos: Pueden iniciar la resolución de reclamos y asignarles un tiempo estimado para su resolución.
Ayuda: Proporciona una guía sobre cómo utilizar el sistema.
Salir: Para cerrar la sesión.
Secretario Técnico
El Secretario Técnico posee todas las funcionalidades de un Jefe de Departamento, y adicionalmente puede cambiar la asignación de departamento para ciertos reclamos.



---

## 🙎‍♂️🙎‍♂️Autores

- Brehm Tomás Nahuel
- Gonzalez Juan Pablo

---

> **Consejo**: Mantén el README **actualizado** conforme evoluciona el proyecto, y elimina (o añade) secciones según necesites. Esta plantilla es sólo un punto de partida general.
