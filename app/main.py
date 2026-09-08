from fastapi import FastAPI
from . import models
from .database import engine
from .routers import projects

# 1. Generate tables in Supabase
models.Base.metadata.create_all(bind=engine)

# 2. Initialize the lean app
app = FastAPI(title="ArthSetu API", version="1.0")

# 3. Plug in the external routes
app.include_router(projects.router)

@app.get("/")
def read_root():
    return {"message": "ArthSetu Core is Online"}