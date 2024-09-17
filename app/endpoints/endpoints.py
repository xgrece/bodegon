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



# Endpoint GET para mostrar el formulario
@router.get("/crear_cliente", response_class=HTMLResponse)
async def show_create_cliente_form(request: Request):
    return templates.TemplateResponse("crear_cliente.html", {"request": request})

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


# Leer un cliente (GET)
@router.get("/clientes/{cliente_id}", response_class=HTMLResponse, tags=["Clientes"])
async def read_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return templates.TemplateResponse("cliente.html", {"request": request, "cliente": cliente})

# Leer todos los clientes (GET)
@router.get("/clientes/", response_class=HTMLResponse, tags=["Clientes"])
async def read_all_clientes(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes = crud.get_all_clientes(db, skip=skip, limit=limit)
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})

# Actualizar un cliente (PUT)
@router.put("/clientes/{cliente_id}", response_class=HTMLResponse, tags=["Clientes"])
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
@router.delete("/clientes/{cliente_id}", response_class=HTMLResponse, tags=["Clientes"])
async def delete_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    crud.delete_cliente(db, cliente_id)
    return templates.TemplateResponse("clientes.html", {"request": request, "message": "Cliente eliminado"})





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
