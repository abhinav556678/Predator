from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .api import events, incidents

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PREDATOR Backend")

# Enable CORS for cross-origin frontend communication (M1 -> M3)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(incidents.router)

@app.get("/")
def read_root():
    return {"message": "PREDATOR API is running"}
