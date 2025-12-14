from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# 1. Definir la URL de conexion
# Usando SQLite (Archivo Local) de forma asincrona (aiosqlite)
SQL_ALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# 2. Creacion del motor asincrono
# El motor maneja la conexion con la DB
engine = create_async_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Sesion de Base de Datos
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# 4. Clase base para modelos
Base = declarative_base()

# 5. Funcion de utilidad para obtener la sesion
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        
# Modelo de la base de datos
class DBTarea(Base):
    __tablename__ = "tareas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)
    
# Funcion para iniciar la base de datos
async def init_db():
    # crear la tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)