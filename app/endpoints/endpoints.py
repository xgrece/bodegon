from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

# Crear un router para clientes
clientes_router = APIRouter()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@clientes_router.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente_data: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db, cliente_data)

@clientes_router.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@clientes_router.get("/clientes/", response_model=list[schemas.Cliente])
def read_all_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_clientes(db, skip=skip, limit=limit)

@clientes_router.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente_data: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    cliente = crud.update_cliente(db, cliente_id, cliente_data.dict())
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@clientes_router.delete("/clientes/{cliente_id}", response_model=dict)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    crud.delete_cliente(db, cliente_id)
    return {"detail": "Cliente eliminado"}

# Crear un router para mesas
mesas_router = APIRouter()

@mesas_router.post("/mesas/", response_model=schemas.Mesa)
def create_mesa(mesa_data: schemas.MesaCreate, db: Session = Depends(get_db)):
    return crud.create_mesa(db, mesa_data)

@mesas_router.get("/mesas/{mesa_id}", response_model=schemas.Mesa)
def read_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = crud.get_mesa(db, mesa_id)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa

@mesas_router.get("/mesas/", response_model=list[schemas.Mesa])
def read_all_mesas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_mesas(db, skip=skip, limit=limit)

@mesas_router.put("/mesas/{mesa_id}", response_model=schemas.Mesa)
def update_mesa(mesa_id: int, mesa_data: schemas.MesaUpdate, db: Session = Depends(get_db)):
    mesa = crud.update_mesa(db, mesa_id, mesa_data.dict())
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa

@mesas_router.delete("/mesas/{mesa_id}", response_model=dict)
def delete_mesa(mesa_id: int, db: Session = Depends(get_db)):
    crud.delete_mesa(db, mesa_id)
    return {"detail": "Mesa eliminada"}