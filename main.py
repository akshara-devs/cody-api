from fastapi import FastAPI

from api.router import api_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Cody API"}


app.include_router(api_router, prefix="/api")
