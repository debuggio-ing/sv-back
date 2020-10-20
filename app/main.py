<<<<<<< HEAD
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
=======
from fastapi import Depends, FastAPI, HTTPException
from pony.schemas import *
from ..pony.models import *
from ..pony.crud import *
from ..api.routes import *


app = routes
>>>>>>> SVM-23 La partición de directorios que me parece correcta
