import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.modelos import Base
from modules.repositorio_concreto import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.gestor_reclamos import GestorDeReclamos
from modules.gestor_usuarios import GestorDeUsuarios

class TestGestorDeReclamos(unittest.TestCase):

    def setUp(self):
        
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.repo_reclamos = RepositorioReclamosSQLAlchemy(self.session)
        self.gestor_reclamos = GestorDeReclamos(self.repo_reclamos)
        self.repo_usuarios = RepositorioUsuariosSQLAlchemy(self.session)
        self.gestor_usuarios = GestorDeUsuarios(self.repo_usuarios)
        
        self.gestor_usuarios.registrar_nuevo_usuario(
            nombre="Juan", 
            email="juan@mail.com", 
            password="clave123",
            apellido="Perez",
            nombre_usuario="juanp",
            claustro="Estudiante",
            rol="Usuario_final"
        )
        self.usuario = self.repo_usuarios.obtener_registro_por_filtro("email", "juan@mail.com")

    def test_agregar_nuevo_reclamo(self):
        self.gestor_reclamos.agregar_nuevo_Reclamo(
            id_creador=self.usuario.id,
            estado="Pendiente",
            tiempo_en_proceso=5,
            contenido="Hay un problema con la luz",
            departamento="Mantenimiento",
            r_imagen = None
            
        )
        reclamos = self.repo_reclamos.obtener_todos_los_registros()
        self.assertEqual(len(reclamos), 1)
        self.assertEqual(reclamos[0].contenido, "Hay un problema con la luz")
        self.assertEqual(reclamos[0].id_creador, self.usuario.id)

    def test_editar_reclamo(self):
        self.gestor_reclamos.agregar_nuevo_Reclamo(
            id_creador=self.usuario.id,
            estado="Pendiente",
            contenido="Problema A",
            departamento="Soporte Informatico",
            tiempo_en_proceso=3
        )
        reclamo = self.repo_reclamos.obtener_todos_los_registros()[0]

        self.gestor_reclamos.editar_Reclamo(
            id_Reclamo=reclamo.id_reclamo,
            id_creador=self.usuario.id,
            estado="En proceso",
            contenido="Problema A",
            departamento="TI",
            tiempo_en_proceso=2,
            r_imagen=reclamo.r_imagen,
            fecha_y_hora=reclamo.fecha_y_hora
        )
        reclamo_editado = self.repo_reclamos.obtener_registro_por_filtro("id_reclamo", reclamo.id_reclamo)
        self.assertEqual(reclamo_editado.estado, "En proceso")

    def test_devolver_reclamo(self):
        self.gestor_reclamos.agregar_nuevo_Reclamo(
            id_creador=self.usuario.id,
            estado="Pendiente",
            contenido="Luz quemada",
            departamento="Maestranza",
            tiempo_en_proceso=2
        )
        reclamo = self.repo_reclamos.obtener_todos_los_registros()[0]
        reclamo_devuelto = self.gestor_reclamos.devolver_Reclamo(reclamo.id_reclamo)
        self.assertIsNotNone(reclamo_devuelto)
        self.assertEqual(reclamo_devuelto.contenido, "Luz quemada")

    def test_listar_reclamos_paginados_sin_departamento(self):
        # Agregar varios reclamos
        for i in range(25):
            self.gestor_reclamos.agregar_nuevo_Reclamo(
                id_creador=self.usuario.id,
                estado="Pendiente",
                contenido=f"Reclamo {i+1}",
                departamento="DeptoA" if i < 15 else "DeptoB",
                tiempo_en_proceso=2
            )
        # Pagina 1, 20 por página
        reclamos, total = self.gestor_reclamos.listar_reclamos_paginados(page=1, per_page=20)
        self.assertEqual(len(reclamos), 20)
        self.assertEqual(total, 25)
        # Cada reclamo debe tener 'n_adherentes' (aunque sea 0)
        for r in reclamos:
            self.assertIn('n_adherentes', r)
            self.assertEqual(r['n_adherentes'], 0)

    def test_listar_reclamos_paginados_con_departamento(self):
        # Agregar reclamos en dos departamentos
        for i in range(10):
            self.gestor_reclamos.agregar_nuevo_Reclamo(
                id_creador=self.usuario.id,
                estado="Pendiente",
                contenido=f"Reclamo {i+1}",
                departamento="Deptox",
                tiempo_en_proceso=2
            )
        for i in range(5):
            self.gestor_reclamos.agregar_nuevo_Reclamo(
                id_creador=self.usuario.id,
                estado="Pendiente",
                contenido=f"Reclamo Y{i+1}",
                departamento="Deptoy",
                tiempo_en_proceso=2
            )
        reclamos, total = self.gestor_reclamos.listar_reclamos_paginados(page=1, per_page=20, departamento="Deptoy")
        self.assertEqual(len(reclamos), 5)
        self.assertEqual(total, 5)
        for r in reclamos:
            self.assertEqual(r['departamento'], "Deptoy")
            self.assertIn('n_adherentes', r)
            self.assertEqual(r['n_adherentes'], 0)

    def test_listar_reclamos_paginados_pagina_vacia(self):
        # No hay reclamos aún
        reclamos, total = self.gestor_reclamos.listar_reclamos_paginados(page=2, per_page=10)
        self.assertEqual(reclamos, [])
        self.assertEqual(total, 0)


    
if __name__ == '__main__':
    unittest.main()