from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="Device Systems",
    description="API REST para la gestión de usuarios",
    version="1.0"
)

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "device_systems API funcionando correctamente"}