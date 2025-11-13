"""
CRUD operations init
Import all CRUD modules here
"""
from app.crud.crud_user import crud_user
from app.crud.crud_ministry import crud_ministry
from app.crud.crud_strategy import crud_strategy

__all__ = ["crud_user", "crud_ministry", "crud_strategy"]

