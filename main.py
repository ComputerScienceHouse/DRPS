from fastapi import FastAPI
from fastapi import FastAPI
from routers import database

app = FastAPI()

app.include_router(database.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
