from app.database import get_db
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract, func, cast, Date


app = FastAPI()

@app.get("/")
async def root():
    return "Hola FastApi"


@app.get("/url")
async def users():
    return {"url": "https://github.com/THOMAS-RIVERA-F?tab=repositories"}

@app.get("/model")
async def predictive_model(db: Session = Depends(get_db)):
    return "Hola Base de datos"



