from fastapi import FastAPI
from app.routes.user import router as UserRouter
from app.routes.delar import router as DelarRouter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = 'http://localhost:8081'
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#USER
app.include_router(UserRouter, tags=["users"], prefix="/api/user")
#DELAR
app.include_router(DelarRouter, tags=["Delars"], prefix="/api/delars")
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return{"status": "server running..!"}

