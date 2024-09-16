from fastapi import APIRouter
from .endpoints import clientes_router, mesas_router, pedidos_router

router = APIRouter()

# Incluye los routers
router.include_router(clientes_router, prefix="/clientes", tags=["clientes"])
router.include_router(mesas_router, prefix="/mesas", tags=["mesas"])
router.include_router(pedidos_router, prefix="/pedidos")