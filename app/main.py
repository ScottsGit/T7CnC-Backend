import uvicorn
from fastapi import FastAPI, APIRouter
from app.database import db

def init_app():
    db.init()
    
    app = FastAPI(
        title= "T7CnC-Backend",
        version= "1"
    )

    @app.on_event("startup")
    async def starup():
        await db.create_all()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()
        
    from app.controller import helloworld
    
    app.include_router(helloworld.router)
        
    return app

app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)