from flask import render_template, request, redirect, url_for, flash, session
from modules.config import app
from modules.gestor_reclamos import GestorDeReclamos
from modules.gestor_usuarios import GestorDeUsuarios
from modules.factoria import crear_repositorio
from modules.analitica import Analitica
from werkzeug.utils import secure_filename
from modules.clasificador import Clasificador
from modules.setup_nltk import prechequeo_nltk
from modules.utils import normalizar_departamento
from flask import send_file
import os

repo_reclamo, repo_usuario = crear_repositorio()
gestor_reclamos = GestorDeReclamos(repo_reclamo)
gestor_usuarios = GestorDeUsuarios(repo_usuario)
prechequeo_nltk.asegurar_recursos_nltk()
clasificador = Clasificador()


#cargar jefes por sistema
'''gestor_usuarios.registrar_nuevo_usuario(
                "nombre", "email", "password", "apellido", "nombre_usuario", "claustro", "rol"
            )
'''


RUTAS_POR_ROL = {
    'Jefe_Secretaria_Tecnica': 'jefe_dashboard',
    'Jefe_Maestranza': 'jefe_dashboard',
    'Jefe_Soporte_Informatico': 'jefe_dashboard',  
    'Usuario_Final': 'usuario_final_dashboard'
}

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        
        if not email or not password:
            flash('Email y contraseña son requeridos', 'danger')
            return render_template('inicio.html')
        
        try:
            usuario = gestor_usuarios.autenticar_usuario(email, password)
            
            if usuario:  
                flash('Inicio de sesión exitoso', 'success')
                session['id'] = usuario.id
                session['rol'] = usuario.rol
                
                
                ruta_destino = RUTAS_POR_ROL.get(usuario.rol, 'inicio')
                return redirect(url_for(ruta_destino))
            else:  
                flash('Email o contraseña incorrectos', 'danger')
                return render_template('inicio.html')
                
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('inicio.html')
        except Exception as e:
            flash('Error interno del servidor', 'danger')
            return render_template('inicio.html')
    
    return render_template('inicio.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        nombre_usuario = request.form.get('nombre_usuario')
        claustro = request.form.get('claustro')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        rol = "Usuario_Final"
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('registrar.html')
        try:
            gestor_usuarios.registrar_nuevo_usuario(
                nombre, email, password, apellido, nombre_usuario, claustro, rol
            )
            flash('Registro exitoso', 'success')
            return redirect(url_for('inicio'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('Error inesperado: ' + str(e), 'danger')
    return render_template('registrar.html')

@app.route('/usuario_final_dashboard')
def usuario_final_dashboard():
    #logica para el dashboard del usuario final
    if 'id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('inicio'))
    id_usuario = session.get('id_usuario')
    return render_template("usuario_final_dashboard.html")

@app.route('/crear_reclamo', methods=['GET', 'POST'])
def crear_reclamo():
    # lógica de creación
    if request.method == 'POST':  
    # 1. Validar sesión
        id_creador = session.get('id')
        if not id_creador:
            flash('Debe iniciar sesión para crear un reclamo', 'danger')
            return redirect(url_for('inicio'))
    # 2. Obtener y validar datos del formulario
        contenido = request.form.get('contenido')
        departamento = clasificador.clasificar([contenido])[0] 
        departamento = normalizar_departamento(departamento) # Parche para unificar los nombres de departamento que devuelve el clasificador y los nombres que utiliza comunmente el codigo
        if not contenido or not contenido.strip():
            flash('El contenido no puede estar vacío', 'danger')
            return render_template('crear_reclamo.html')  
        if not departamento:
            flash('Hubo un error al clasificar su departamento', 'danger')
            return render_template('crear_reclamo.html')    
    # 3. Inicializar variables
        estado = "Pendiente"
        tiempo_en_proceso = None
        r_imagen = None
    # 4. Manejo de imagen (si existe)
        imagen = request.files.get("imagen")
        if imagen and imagen.filename:
            # Validar tipo de archivo
            if not imagen.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                flash('Solo se permiten archivos de imagen (PNG, JPG, JPEG, GIF)', 'danger')
                return render_template('crear_reclamo.html')
            filename = secure_filename(imagen.filename)
            ruta_directorio = "static/images/reclamos"
            # Crear directorio si no existe
            os.makedirs(ruta_directorio, exist_ok=True)
            ruta_completa = os.path.join(ruta_directorio, filename)
            imagen.save(ruta_completa)
            r_imagen = f"images/reclamos/{filename}"
    # 5 Busqueda de reclamos similares
        reclamos_similares = gestor_reclamos.obtener_reclamos_departamento(departamento)
        if reclamos_similares:
            # Guardar temporalmente los datos del nuevo reclamo en la sesión
            session['nuevo_reclamo'] = {
                'id_creador': id_creador,
                'contenido': contenido,
                'departamento': departamento,
                'r_imagen': r_imagen
            }
            # Mostrar lista de reclamos similares para decidir si adherirse
            return render_template("reclamos_similares.html", similares=reclamos_similares)
        else: 
            # Si no hay similares, se crea directamento
            try:
                gestor_reclamos.agregar_nuevo_Reclamo(id_creador, estado, contenido, departamento, tiempo_en_proceso,r_imagen)
                flash('Reclamo creado exitosamente', 'success')
                return redirect(url_for('listar_reclamos'))
            except ValueError as e:
                flash(str(e), 'danger')
    return render_template("crear_reclamo.html")

@app.route('/confirmar_reclamo', methods=['POST'])
def confirmar_reclamo():
    decision = request.form.get('decision')  # "adherir" o "nuevo"
    reclamo_id = request.form.get('reclamo_id')  # si se adhiere
    nuevo = session.get('nuevo_reclamo')
    if not nuevo:
        flash('No se encontró la información del nuevo reclamo', 'danger')
        return redirect(url_for('crear_reclamo'))
    if decision == "adherir" and reclamo_id:
        try:
            gestor_usuarios.registrar_reclamo_a_seguir(nuevo['id_creador'], int(reclamo_id))
            flash('Te adheriste a un reclamo existente', 'success')
        except ValueError as e:
            flash(str(e), 'danger')
    else:
        gestor_reclamos.agregar_nuevo_Reclamo(
            id_creador=nuevo['id_creador'],
            estado="Pendiente",
            contenido=nuevo['contenido'],
            departamento=nuevo['departamento'],
            tiempo_en_proceso=None,
            r_imagen=nuevo['r_imagen']
        )
        flash('Reclamo creado exitosamente', 'success')
    session.pop('nuevo_reclamo', None)
    return redirect(url_for('listar_reclamos'))

@app.route('/listar_reclamos')
def listar_reclamos():
    if 'id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('inicio'))
    page = request.args.get('page', 1, type=int)
    per_page = 20
    departamento = request.args.get('departamento')
    try:
        reclamos, total = gestor_reclamos.listar_reclamos_paginados(page=page, per_page=per_page,departamento=departamento)
        return render_template("listar_reclamos.html", reclamos=reclamos, page=page, per_page=per_page, total=total)
    except Exception as e:
        flash(str(e), 'danger')
        return render_template("listar_reclamos.html", reclamos=[], page=1, per_page=per_page, total=0)



@app.route('/adherirse/<int:id_reclamo>', methods=['POST'])
def adherirse_a_reclamo(id_reclamo):
    if 'id' not in session:
        flash('Debes iniciar sesión para adherirte a un reclamo.', 'warning')
        return redirect(url_for('inicio'))
    
    id_usuario = session.get('id')
    try:
        #AGREGAR LOGICA PARA QUE UN USUARIO NO PUEDA ADHERIRSE A SU PROPIO RECLAMO
        if gestor_reclamos.devolver_Reclamo(id_reclamo).id_creador == id_usuario:
            flash('No puedes adherirte a tu propio reclamo.', 'warning')
            return redirect(url_for('listar_reclamos'))
        gestor_usuarios.registrar_reclamo_a_seguir(id_usuario, id_reclamo)
        flash('Te adheriste correctamente al reclamo.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('listar_reclamos'))


@app.route('/mis_reclamos')
def mis_reclamos():
    # lógica para ver solo los reclamos del usuario actual
    if 'id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('inicio'))
    id_usuario = session.get('id')
    try:
        reclamos = gestor_reclamos.devolver_reclamos_segun_usuario(id_usuario)
        return render_template("mis_reclamos.html", reclamos=reclamos)
    except Exception as e:
        flash('Error al listar los reclamos: ' + str(e), 'danger')
    return render_template("mis_reclamos.html")

@app.route('/jefe_dashboard')
def jefe_dashboard():
    if 'id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('inicio'))
    
    return render_template(
        'jefe_dashboard.html',
        dpto = session['rol'].removeprefix("Jefe_"),
        rol = session['rol']
    )

@app.route('/analiticas/<departamento>')
def ver_analiticas(departamento):
    # Validación: el usuario debe estar logueado
    if 'id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('inicio'))

    # Generar estadísticas del departamento
    analitica = Analitica(repo_reclamo)  
    stats = analitica.generar_estadisticas(departamento)

    return render_template(
        'ver_analiticas.html',  
        departamento=departamento,
        total=stats["total"],
        porcentajes=stats["porcentajes"],
        mediana_proceso=stats["mediana_proceso"], 
        mediana_resueltos=stats["mediana_resueltos"],
        ruta_nube=stats["ruta_nube"],
        ruta_torta=stats["ruta_torta"]
    )


@app.route('/manejar_reclamos/<departamento>')
def manejar_reclamos(departamento):
    page = request.args.get('page', 1, type=int)
    per_page = 20
    rol = session.get('rol')
    try:
        reclamos, total = gestor_reclamos.listar_reclamos_paginados(page=page, per_page=per_page, departamento=departamento)
        return render_template("manejar_reclamos.html", reclamos=reclamos,departamento=departamento, page=page, per_page=per_page, total=total, rol=rol)
    except Exception as e:
        flash(str(e), 'danger')
        return render_template("manejar_reclamos.html", reclamos=[], departamento=departamento, page=1, per_page=per_page, total=0)


@app.route('/iniciar_resolucion/<int:id_reclamo>', methods=['GET', 'POST'])
def iniciar_resolucion(id_reclamo):
    if 'id' not in session:
        flash("Debes iniciar sesión", "warning")
        return redirect(url_for('inicio'))

    reclamo = gestor_reclamos.devolver_Reclamo(id_reclamo)
    if not reclamo:
        flash("Reclamo no encontrado", "danger")
        return redirect(url_for('manejar_reclamos', departamento=reclamo.departamento))

    if request.method == 'POST':
        estado = request.form.get('nuevo_estado') 
        
        if estado == "En proceso":
            tiempo_resolucion = request.form.get('tiempo_resolucion')
            if not tiempo_resolucion or not tiempo_resolucion.isdigit():
                flash("El tiempo de resolución debe ser un número válido", "danger")
                return render_template("resolver_reclamo.html", reclamo=reclamo)
            tiempo_resolucion = int(tiempo_resolucion)
        elif estado == "Resuelto":
            tiempo_resolucion = reclamo.tiempo_en_proceso
        
        elif estado == "Invalido":
            tiempo_resolucion = None

        try:
            gestor_reclamos.editar_Reclamo(
                reclamo.id_reclamo,
                reclamo.id_creador,
                estado,
                reclamo.contenido,
                reclamo.departamento,
                tiempo_resolucion,
                reclamo.r_imagen,
                reclamo.fecha_y_hora
            )
            flash("Reclamo actualizado correctamente", "success")
            return redirect(url_for('manejar_reclamos', departamento=reclamo.departamento))
        except Exception as e:
            flash(f"Error al actualizar: {str(e)}", "danger")

    return render_template("resolver_reclamo.html", reclamo=reclamo)


@app.route('/derivar_reclamo/<int:id_reclamo>', methods=['POST'])
def derivar_reclamo(id_reclamo):
    if session.get('rol') != 'Jefe_Secretaria_Tecnica':
        flash("No tiene permisos para realizar esta acción", "danger")
        return redirect(url_for('listar_reclamos'))
    try:
        nuevo_dpto = request.form.get('nuevo_dpto')
    except Exception as e:
        flash(f"No fue posible encontrar el nuevo departamento: {str (e)}")

    try:
        reclamo = gestor_reclamos.devolver_Reclamo(id_reclamo)
    except Exception as e:
        flash(f"Error al encontrar el reclamo por id: {str(e)}", "danger")
        return redirect()

    if nuevo_dpto not in ['Maestranza', 'Soporte_Informatico']:
        flash("Departamento no válido", "danger")
        return redirect(url_for('manejar_reclamos',departamento = reclamo.departamento))

    if reclamo and reclamo.id_reclamo == id_reclamo:
        try:
            gestor_reclamos.editar_Reclamo(id_reclamo,
                                        reclamo.id_creador,
                                        reclamo.estado,
                                        reclamo.contenido, 
                                        nuevo_dpto,
                                        reclamo.tiempo_en_proceso,
                                        reclamo.r_imagen,
                                        reclamo.fecha_y_hora)
            flash("Reclamo derivado correctamente", "success")
        except Exception as e:
            flash(f"Error al derivar el reclamo: {str(e)}", "danger")

    return redirect(url_for('manejar_reclamos',departamento = reclamo.departamento))

@app.route('/analiticas/<departamento>/reporte.<formato>')
def descargar_reporte(departamento, formato):
    if 'id' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('inicio'))

    analitica = Analitica(repo_reclamo)

    try:
        buffer, mime, filename = analitica.exportar_archivo(departamento, formato)
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('jefe_dashboard'))

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype=mime
    )

@app.route('/logout')
def logout():
    session.clear() 
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('inicio'))


if __name__ == "__main__": app.run(debug=True, host='0.0.0.0')
    
    
