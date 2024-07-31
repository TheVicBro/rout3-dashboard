from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.myapi import router as myapi_router
from app.api.routers.secrets import router as secrets_router
from app.api.routers.token import router as token_router
from app.api.routers.user import router as user_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(secrets_router)
app.include_router(token_router)
app.include_router(myapi_router)


@app.get("/")
def root():
    return "Server is running"
