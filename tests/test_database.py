from app.database.connection import Base, engine

# Crear todas las tablas definidas en los modelos
print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas con éxito.")
