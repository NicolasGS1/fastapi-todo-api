from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
# Import para la base de datos y la configuracion de la misma
from database import DBTarea, get_db, init_db

app = FastAPI()
# --- Modelo de Pydantic (Lo que el cliente envia/recibe)
class Tarea(BaseModel):
    # el ID es opcional al crear, pero existe
    id: Optional[int] = None
    titulo: str
    descripcion: Optional[str] = None
    completada: bool = False

#-- Hooks de la aplicacion --
# Llama esta funcion cuando la API inicie para crear la tabla
@app.on_event("startup")
async def startup_event():
    await init_db()
    print("Base de datos inicializada y tablas creadas.")

#--ENDPOINTS (RUTAS)--
# Mensaje de bienvenida
@app.get("/")
def home():
    return {"Mensaje": "Bienvenido a mi API de Tareas"}

# 1. Obtiene todas las tareas (GET)
@app.get("/todos", response_model=List[Tarea])
async def obtener_tareas(db: AsyncSession = Depends(get_db)):
    # Usamos SQLAlchemy para hacer un SELECT
    resultado = await db.execute(select(DBTarea))
    tareas_db = resultado.scalars().all()
    return tareas_db

# 2. Crea una nueva tarea (POST)
@app.post("/todos", response_model=Tarea, status_code=201)
async def crear_tarea(tarea: Tarea, db: AsyncSession = Depends(get_db)):
    #Se convierte el modelo Pydantic al modelo de DB
    nueva_tarea_db = DBTarea(
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        completada=tarea.completada
    )
    db.add(nueva_tarea_db)
    await db.commit()
    await db.refresh(nueva_tarea_db) # Se obtiene el ID que genero la DB
    return nueva_tarea_db

# 3. Actualizar una tarea (Ruta PUT)
@app.put("/todos/{tarea_id}", response_model=Tarea)
async def actualizar_tarea(tarea_id: int, tarea, db: AsyncSession = Depends(get_db)):
    # 1. Busca la tarea
    stmt_select = select (DBTarea).filter(DBTarea.id == tarea_id)
    resultado = await db.execute(stmt_select)
    tarea_db = resultado.scalar_one_or_none()
    
    if tarea_db is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # 2. Actualizar los campos
    tarea_db.titulo = tarea.titulo
    tarea_db.descripcion = tarea.descripcion
    tarea_db.completada = tarea.completada
    
    await db.commit()
    await db.refresh(tarea_db)
    return tarea_db


# 4. Eliminar una tarea por el ID
@app.delete("/todos/{tarea_id}", status_code=204)
async def eliminar_tarea(tarea_id: int, db: AsyncSession = Depends(get_db)):
    # 1. Buscar y eliminar
    # Se usa filter_by para simplificar la sintaxis si solo es un campo
    stmt_delete = delete(DBTarea).filter_by(id=tarea_id)
    
    resultado = await db.execute(stmt_delete)
    
    #2. Confirmar la accion de eliminar
    await db.commit()
    
    if resultado.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Si todo esta bien se envia el codigo 204 automaticamente
    return {"ok": True}    