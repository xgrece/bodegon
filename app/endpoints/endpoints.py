from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from typing import List

# Crear un router para clientes
clientes_router = APIRouter()
# Crear un router para mesas
mesas_router = APIRouter()
# Crear un router para pedidos
pedidos_router = APIRouter()

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


@pedidos_router.post("/pedidos/", response_model=schemas.Pedido, tags=["pedidos"])
def create_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return crud.create_pedido(db=db, pedido=pedido)

@pedidos_router.get("/pedidos/", response_model=List[schemas.Pedido], tags=["pedidos"])
def read_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_pedidos(db, skip=skip, limit=limit)

@pedidos_router.get("/pedidos/{pedido_id}", response_model=schemas.Pedido, tags=["pedidos"])
def read_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return crud.get_pedido(db, pedido_id=pedido_id)

@pedidos_router.put("/pedidos/{pedido_id}", response_model=schemas.Pedido, tags=["pedidos"])
def update_pedido(pedido_id: int, pedido: schemas.PedidoUpdate, db: Session = Depends(get_db)):
    return crud.update_pedido(db=db, pedido_id=pedido_id, pedido=pedido)

@pedidos_router.delete("/pedidos/{pedido_id}", tags=["pedidos"])
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return crud.delete_pedido(db=db, pedido_id=pedido_id)