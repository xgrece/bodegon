from sqlalchemy.orm import Session
from .models import Cliente, Mesa
from .schemas import ClienteCreate, ClienteUpdate, MesaCreate, MesaUpdate

def create_cliente(db: Session, cliente_data: ClienteCreate):
    db_cliente = Cliente(**cliente_data.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def get_all_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cliente).offset(skip).limit(limit).all()

def update_cliente(db: Session, cliente_id: int, cliente_data: ClienteUpdate):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        for key, value in cliente_data.dict().items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    return None

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        db.delete(db_cliente)
        db.commit()

def create_mesa(db: Session, mesa_data: MesaCreate):
    db_mesa = Mesa(**mesa_data.dict())
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

def get_mesa(db: Session, mesa_id: int):
    return db.query(Mesa).filter(Mesa.id == mesa_id).first()

def get_all_mesas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Mesa).offset(skip).limit(limit).all()

def update_mesa(db: Session, mesa_id: int, mesa_data: MesaUpdate):
    db_mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if db_mesa:
        for key, value in mesa_data.dict().items():
            setattr(db_mesa, key, value)
        db.commit()
        db.refresh(db_mesa)
        return db_mesa
    return None

def delete_mesa(db: Session, mesa_id: int):
    db_mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if db_mesa:
        db.delete(db_mesa)
        db.commit()