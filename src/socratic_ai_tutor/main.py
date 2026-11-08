from fastapi import FastAPI
from .api.tutor import router

app = FastAPI()

app.include_router(router)

@app.get('/')
def root():
    return {"root"}