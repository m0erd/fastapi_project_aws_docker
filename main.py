from fastapi import FastAPI
from healthai.src.api.ledgers.router import router as healthai_router
from travelai.src.api.ledgers.router import router as travelai_router

app = FastAPI()

app.include_router(healthai_router, prefix="/healthai")
app.include_router(travelai_router, prefix="/travelai")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
