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
from app.endpoints import clientes_router, mesas_router, pedidos_router

# Iniciar el server:  uvicorn app.main:app --reload
# uvicorn app.main:app --reload

# detener el server: CTRL+C

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de Jinja2Templates para usar la carpeta 'templates'
templates = Jinja2Templates(directory="app/templates")

# Montar la carpeta static para servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
app.include_router(pedidos_router, prefix="/pedidos")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#---------------------- CLIENTES ---------------------------------------------------------
# Crear un cliente (POST)
@app.post("/clientes/", response_class=HTMLResponse)
async def create_cliente(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    cliente_data = schemas.ClienteCreate(nombre=nombre, apellido=apellido, email=email)
    cliente = crud.create_cliente(db, cliente_data)
    return templates.TemplateResponse("cliente.html", {"request": request, "cliente": cliente})

# Leer un cliente (GET)
@app.get("/clientes/{cliente_id}", response_class=HTMLResponse)
async def read_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return templates.TemplateResponse("cliente.html", {"request": request, "cliente": cliente})

# Leer todos los clientes (GET)
@app.get("/clientes/", response_class=HTMLResponse)
async def read_all_clientes(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes = crud.get_all_clientes(db, skip=skip, limit=limit)
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})

# Actualizar un cliente (PUT)
@app.put("/clientes/{cliente_id}", response_class=HTMLResponse)
async def update_cliente(
    request: Request,
    cliente_id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    cliente_data = schemas.ClienteUpdate(nombre=nombre, apellido=apellido, email=email)
    cliente = crud.update_cliente(db, cliente_id, cliente_data)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return templates.TemplateResponse("cliente.html", {"request": request, "cliente": cliente})

# Eliminar un cliente (DELETE)
@app.delete("/clientes/{cliente_id}", response_class=HTMLResponse)
async def delete_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    crud.delete_cliente(db, cliente_id)
    return templates.TemplateResponse("clientes.html", {"request": request, "message": "Cliente eliminado"})

#---------------------- MESAS ------------------------------------------------------------
@app.post("/mesas/", response_class=HTMLResponse)
def create_mesa(request: Request, mesa_data: schemas.MesaCreate, db: Session = Depends(get_db)):
    mesa = crud.create_mesa(db, mesa_data)
    return templates.TemplateResponse("mesa.html", {"request": request, "mesa": mesa})

@app.get("/mesas/{mesa_id}", response_class=HTMLResponse)
def read_mesa(request: Request, mesa_id: int, db: Session = Depends(get_db)):
    mesa = crud.get_mesa(db, mesa_id)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return templates.TemplateResponse("mesa.html", {"request": request, "mesa": mesa})

@app.get("/mesas/", response_class=HTMLResponse)
def read_all_mesas(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mesas = crud.get_all_mesas(db, skip=skip, limit=limit)
    return templates.TemplateResponse("mesas.html", {"request": request, "mesas": mesas})

@app.put("/mesas/{mesa_id}", response_class=HTMLResponse)
def update_mesa(request: Request, mesa_id: int, mesa_data: schemas.MesaUpdate, db: Session = Depends(get_db)):
    mesa = crud.update_mesa(db, mesa_id, mesa_data)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return templates.TemplateResponse("mesa.html", {"request": request, "mesa": mesa})

@app.delete("/mesas/{mesa_id}", response_class=HTMLResponse)
def delete_mesa(request: Request, mesa_id: int, db: Session = Depends(get_db)):
    crud.delete_mesa(db, mesa_id)
    return templates.TemplateResponse("mesas.html", {"request": request, "message": "Mesa eliminada"})



#---------------------- PEDIDOS ---------------------------------------------------------
# Lista global para almacenar los pedidos
pedidos = []

@app.get("/pedido", response_class=HTMLResponse)
async def read_pedido(request: Request):
    return templates.TemplateResponse("pedido.html", {"request": request, "pedidos": pedidos})

@app.post("/create_pedido", response_class=HTMLResponse)
async def create_pedido(request: Request, mesa: int = Form(...), producto: str = Form(...)):
    pedidos.append({"mesa": mesa, "producto": producto})
    return templates.TemplateResponse("pedido.html", {"request": request, "pedidos": pedidos, "message": "Pedido creado exitosamente!"})


#---------------------- I C O N ---------------------------------------------------------  
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/assets/favicon.ico")
