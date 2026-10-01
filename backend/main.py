from fastapi import FastAPI
from . import models
from .database import engine
from .api import events, incidents

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PREDATOR Backend")

app.include_router(events.router)
app.include_router(incidents.router)

@app.get("/")
def read_root():
    return {"message": "PREDATOR API is running"}
