from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.secrets import router as secrets_router
from api.routers.user import router as user_router
from api.routers.token import router as token_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(secrets_router)
app.include_router(token_router)


@app.get("/")
def root():
    return "Server is running"
