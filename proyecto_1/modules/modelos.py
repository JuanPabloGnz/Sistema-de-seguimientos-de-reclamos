from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()

asociacion_usuarios_reclamos = Table('usuarios_reclamos', Base.metadata,
    Column('id_usuario', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('id_reclamo', Integer, ForeignKey('reclamos.id_reclamo'), primary_key=True)
)

class ModeloReclamo(Base):
    """Modelo que representa un reclamo en la base de datos."""
    __tablename__ = 'reclamos'
    id_reclamo = Column(Integer(), primary_key=True)
    id_creador = Column(Integer(), nullable=False)
    estado = Column(String(20), nullable=False)
    contenido = Column(String(1000), nullable=False)
    r_imagen = Column(String(255))
    fecha_y_hora = Column(DateTime, nullable=False, default=func.now())
    departamento = Column(String(50))
    tiempo_en_proceso = Column(Integer())

class ModeloUsuario(Base):
    """Modelo que representa un usuario en la base de datos."""
    __tablename__ = 'usuarios'
    id = Column(Integer(), primary_key=True, autoincrement=True) 
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    nombre_usuario = Column(String(30), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    claustro = Column(String(20))
    rol = Column(String(50), nullable =False) #CAMBIAR ESTO




    reclamos_adheridos = relationship('ModeloReclamo', secondary=asociacion_usuarios_reclamos, backref= 'usuarios_adherentes')