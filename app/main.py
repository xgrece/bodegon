from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, crud, schemas
from datetime import date
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from app.endpoints import router as endpoints_router
from app.endpoints import clientes_router, mesas_router

# Iniciar el server: uvicorn main:app --reload
# uvicorn app.main:app --reload

# detener el server: CTRL+C

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de Jinja2Templates para usar la carpeta 'templates'
templates = Jinja2Templates(directory="app/templates")

# Montar la carpeta static para servir archivos estáticos
#app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(endpoints_router)
app.include_router(clientes_router, prefix="/api")
app.include_router(mesas_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#---------------------- CLIENTES ---------------------------------------------------------
@app.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente_data: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db, cliente_data)

@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.get("/clientes/", response_model=list[schemas.Cliente])
def read_all_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_clientes(db, skip=skip, limit=limit)

@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente_data: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    cliente = crud.update_cliente(db, cliente_id, cliente_data)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.delete("/clientes/{cliente_id}", response_model=dict)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    crud.delete_cliente(db, cliente_id)
    return {"detail": "Cliente eliminado"}

#---------------------- MESAS ------------------------------------------------------------
@app.post("/mesas/", response_model=schemas.Mesa)
def create_mesa(mesa_data: schemas.MesaCreate, db: Session = Depends(get_db)):
    return crud.create_mesa(db, mesa_data)

@app.get("/mesas/{mesa_id}", response_model=schemas.Mesa)
def read_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = crud.get_mesa(db, mesa_id)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa

@app.get("/mesas/", response_model=list[schemas.Mesa])
def read_all_mesas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_mesas(db, skip=skip, limit=limit)

@app.put("/mesas/{mesa_id}", response_model=schemas.Mesa)
def update_mesa(mesa_id: int, mesa_data: schemas.MesaUpdate, db: Session = Depends(get_db)):
    mesa = crud.update_mesa(db, mesa_id, mesa_data)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa

@app.delete("/mesas/{mesa_id}", response_model=dict)
def delete_mesa(mesa_id: int, db: Session = Depends(get_db)):
    crud.delete_mesa(db, mesa_id)
    return {"detail": "Mesa eliminada"}