import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.database import db
from app.config import API_V1_STR

def init_app():
    db.init()
    
    def custom_generate_unique_id(route: APIRoute) -> str:
        return f"{route.tags[0]}-{route.name}"

    app = FastAPI(
        title= "T7CnC-Backend",
        openapi_url=f"{API_V1_STR}/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
        version= "1",
    )

    @app.on_event("startup")
    async def starup():
        await db.create_all()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()
        
    from app.controller import helloworld, userController
    
    app.include_router(helloworld.router)
    app.include_router(userController.router)
        
    return app

app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)