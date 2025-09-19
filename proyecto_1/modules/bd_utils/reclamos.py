from sqlalchemy import update
from modules.modelos import ModeloReclamo 
from sqlalchemy import create_engine, update, text
from sqlalchemy.orm import sessionmaker

# Estas lineas de codigo solo se ejecutan para solucionar un error puntual. Por lo tanto, no es necesario crear un
# método nuevo en el RepositorioConcreto. El error se daba porque anteriormente se inicializaban los reclamos 
# con un valor de tiempo_en_proceso == 0, y ahora lo cambiamos a None para evitar problemas con restricciones 
# en la base de datos. 
# Por ende, se procede a modificar todos los registros viejos que tenian un tiempo_en_proceso == 0 por None.


# Crear engine y sesión una sola vez
engine = create_engine('sqlite:///data/base_datos.db')
Session = sessionmaker(bind=engine)
session = Session()

# 1. Actualizar tiempo_en_proceso = 0 → None
session.execute(
    update(ModeloReclamo)
    .where(ModeloReclamo.departamento == 'Secretaría Técnica')
    .values(departamento='Secretaria_Tecnica')
)
session.commit()

# # 2. Eliminar columna 'clasificacion' con SQL directo
# with engine.connect() as conn:
#     conn.execute(text("ALTER TABLE reclamos DROP COLUMN clasificacion"))

# session.close()