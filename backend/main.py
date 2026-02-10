from fastapi import FastAPI
from simulate.routes import router as simulate_router
from auth.routes import router as auth_router



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sqlmodel import SQLModel

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://magnathon-six.vercel.app",
        "https://magnathon.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

""" 
    ROUTERS
"""
app.include_router(simulate_router)
app.include_router(auth_router)


@app.get("/")
def health_check():
    return {"Message" : "Server is listening"}