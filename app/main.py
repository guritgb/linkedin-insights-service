from fastapi import FastAPI
from app.database.mongodb import db
from app.routes.page_routes import page_router

app = FastAPI()

@app.get("/")
def check():
    return{
        "message":"connected"
    }


app.include_router(page_router)