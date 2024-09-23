from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

from fastapi.templating import Jinja2Templates

# Crear un router principal
router = APIRouter()

# Crear un objeto Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#=============================== CLIENTES ================================================

@router.get("/crear_cliente", response_class=HTMLResponse)
async def show_create_cliente_form(request: Request):
    return templates.TemplateResponse("crear_cliente.html", {"request": request})

<<<<<<< HEAD
=======

# Endpoint GET para mostrar el formulario
@router.get("/crear_cliente", response_class=HTMLResponse)
async def show_create_cliente_form(request: Request):
    return templates.TemplateResponse("crear_cliente.html", {"request": request})

>>>>>>> 064548502e1714fe104b9fcdf5c5b034cea2e549
@router.post("/crear_cliente", response_class=HTMLResponse)
async def create_cliente(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    cliente_data = schemas.ClienteCreate(nombre=nombre, apellido=apellido, email=email)
    cliente = crud.create_cliente(db, cliente_data)
    return templates.TemplateResponse("crear_cliente.html", {
        "request": request, 
        "message": f"Cliente {nombre} {apellido} creado exitosamente"
    })
<<<<<<< HEAD
    
@router.get("/read_clientes", response_class=HTMLResponse)
async def read_clientes(request: Request, db: Session = Depends(get_db)):
    clientes = crud.get_all_clientes(db)
    return templates.TemplateResponse("read_clientes.html", {"request": request, "clientes": clientes})
=======

>>>>>>> 064548502e1714fe104b9fcdf5c5b034cea2e549

# Obtener un cliente por ID (GET)
@router.get("/clientes/{cliente_id}", response_class=HTMLResponse)
async def get_cliente_by_id(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    # Asumiendo que `cliente` es un objeto HTML que se puede renderizar
    return HTMLResponse(content=f"<html><body><h1>Cliente {cliente_id}</h1><p>{cliente}</p></body></html>")

# Actualizar un cliente (POST)
@router.post("/clientes/{cliente_id}/actualizar", response_class=HTMLResponse)
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
    return templates.TemplateResponse("clientes.html", {"request": request, "message": f"Cliente {nombre} {apellido} actualizado correctamente"})

# Eliminar un cliente (POST)
@router.post("/clientes/{cliente_id}/eliminar", response_class=HTMLResponse)
async def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    result = crud.delete_cliente(db, cliente_id)

    if result.get("status") == "success":
        return HTMLResponse(content="Cliente eliminado", status_code=200)
    else:
        return HTMLResponse(content="Error al eliminar el cliente", status_code=400)

#======================================= MESAS ========================================
@router.post("/mesas/", response_class=HTMLResponse, tags=["Mesas"])
def create_mesa(request: Request, mesa_data: schemas.MesaCreate, db: Session = Depends(get_db)):
    mesa = crud.create_mesa(db, mesa_data)
    return templates.TemplateResponse("mesa.html", {"request": request, "mesa": mesa})

@router.get("/mesas/{mesa_id}", response_class=HTMLResponse, tags=["Mesas"])
def read_mesa(request: Request, mesa_id: int, db: Session = Depends(get_db)):
    mesa = crud.get_mesa(db, mesa_id)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return templates.TemplateResponse("mesa.html", {"request": request, "mesa": mesa})

@router.get("/mesas/", response_class=HTMLResponse, tags=["Mesas"])
def read_all_mesas(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mesas = crud.get_all_mesas(db, skip=skip, limit=limit)
    return templates.TemplateResponse("mesas.html", {"request": request, "mesas": mesas})

@router.put("/mesas/{mesa_id}", response_class=HTMLResponse, tags=["Mesas"])
def update_mesa(request: Request, mesa_id: int, mesa_data: schemas.MesaUpdate, db: Session = Depends(get_db)):
    mesa = crud.update_mesa(db, mesa_id, mesa_data)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return templates.TemplateResponse("mesa.html", {"request": request, "mesa": mesa})

@router.delete("/mesas/{mesa_id}", response_class=HTMLResponse, tags=["Mesas"])
def delete_mesa(request: Request, mesa_id: int, db: Session = Depends(get_db)):
    crud.delete_mesa(db, mesa_id)
    return templates.TemplateResponse("mesas.html", {"request": request, "message": "Mesa eliminada"})





#======================================= PEDIDOS ========================================
# Lista global para almacenar los pedidos
pedidos = []

@router.post("/create_pedido", response_class=HTMLResponse, tags=["Pedidos"])
async def create_pedido(request: Request, mesa: int = Form(...), producto: str = Form(...)):
    pedidos.append({"mesa": mesa, "producto": producto})
    return templates.TemplateResponse("pedido.html", {"request": request, "pedidos": pedidos, "message": "Pedido creado exitosamente!"})

@router.get("/pedido", response_class=HTMLResponse, tags=["Pedidos"])
async def read_pedido(request: Request):
    return templates.TemplateResponse("pedido.html", {"request": request, "pedidos": pedidos})
