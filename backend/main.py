from fastapi import FastAPI
from simulate.routes import router as simulate_router
from auth.routes import router as auth_router



app = FastAPI()

""" 
    ROUTERS
"""
app.include_router(simulate_router)
app.include_router(auth_router)


@app.get("/")
def health_check():
    return {"Message" : "Server is listening"}