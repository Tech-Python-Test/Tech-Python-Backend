from fastapi import FastAPI
from app.routers import user, conversation, message, group, event
from app.database.connection import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Inicializar la aplicación FastAPI
app = FastAPI()

# Crear las tablas en la base de datos si aún no existen
Base.metadata.create_all(bind=engine)

# Incluir los routers
app.include_router(user.router)
app.include_router(conversation.router)
app.include_router(message.router)
app.include_router(group.router)
app.include_router(event.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Cambia esto según el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de prueba para verificar si el servidor está funcionando
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}
