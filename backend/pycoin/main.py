from fastapi import FastAPI

from pycoin.config import get_settings

from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "PyCoin is an educational cryptocurrency and decentralized blockchain project."
    ),
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


@app.get("/api/v1/health", tags=["System"])
async def health_check():
    return {
        "success": True,
        "message": "PyCoin API is running",
        "data": {
            "status": "healthy",
            "application": settings.app_name,
            "version": settings.app_version,
            "coin": settings.coin_symbol,
        },
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "application": settings.app_name,
        "symbol": settings.coin_symbol,
        "message": "Welcome to PyCoin",
        "documentation": "/docs",
    }
