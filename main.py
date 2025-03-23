from fastapi import FastAPI
from healthai.src.api.ledgers.router import router as healthai_router
from travelai.src.api.ledgers.router import router as travelai_router
from sqlalchemy import create_engine
import os

db_password = os.getenv("DB_PASSWORD")

app = FastAPI()

# DB_HOST = "postgres_db"
# DB_PORT = "5432"
# DB_NAME = "fastapi_db"
# DB_USER = "user"
# DB_PASS = db_password
#
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# engine = create_engine(DATABASE_URL)

app.include_router(healthai_router, prefix="/healthai")
app.include_router(travelai_router, prefix="/travelai")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# from fastapi import FastAPI
# from healthai.src.api.ledgers.router import router as healthai_router
# from travelai.src.api.ledgers.router import router as travelai_router
#
# app = FastAPI()
#
# app.include_router(healthai_router, prefix="/healthai")
# app.include_router(travelai_router, prefix="/travelai")
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
