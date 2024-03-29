import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from app.database import db
from app.config import API_V1_STR

origins= [
    "http://localhost:3000",
    '*'
]

def init_app():
    db.init()

    app = FastAPI(
        title= "T7CnC-Backend",
        version= "1",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def starup():
        await db.create_all()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()
        
    from app.controller import helloworld, auth, user, plaid_controller
    
    app.include_router(helloworld.router)
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(plaid_controller.router)
        
    return app

app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)