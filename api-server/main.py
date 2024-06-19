from fastapi import FastAPI
from fastapi.security import HTTPBasic
from fastapi.middleware.cors import CORSMiddleware
from routers.secrets import router as secrets_router
from routers.user import router as user_router


app = FastAPI()
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(secrets_router)


@app.get("/")
def root():
    return "Server is running"
