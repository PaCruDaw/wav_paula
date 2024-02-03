from typing import Union
from fastapi import FastAPI
from app.db_config.database import Base
from app.db_config.database import engine
from app.controllers import login
from app.security.secure import get_current_valid_user
from app.models.data.sqlalchemy_models import Users
from fastapi import Security

app = FastAPI()

def configure():
    app.include_router(login.router, prefix="/login")
    
configure()

Base.metadata.create_all(bind=engine) 

@app.get("/products")
def read_root(current_user: Users = Security(get_current_valid_user)):
    return {"producte1": "asdfasdfsadfdsaf"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "qss": q}


    