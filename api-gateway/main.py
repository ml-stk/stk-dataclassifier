from fastapi import FastAPI
from api-gateway.routers.files import router as files_router

app = FastAPI(title="STK Data Classification Platform", version="1.0.0")

app.include_router(files_router)

@app.get("/")
def health_check():
    return {"status": "running", "environment": "STK Trial VM"}