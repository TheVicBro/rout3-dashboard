from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.setup import init_db


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins

allowed_origins = [
    "https://rout3.vercel.app",
    "https://rout3.com",
    "https://www.rout3.com",
    "https://rout3-dev.vercel.app",
]

# If there are additional origins in settings.BACKEND_CORS_ORIGINS, include them as well
if settings.BACKEND_CORS_ORIGINS:
    allowed_origins.extend(
        [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


# Bind Tables and add first user to db
@app.on_event("startup")
async def startup_event():
    init_db()