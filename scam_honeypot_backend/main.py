from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.core.config import settings
from app.core.lifecycle import lifespan
from app.core.security import RateLimiter
from app.api.routes import router as api_router
from starlette.requests import Request
from starlette.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Skip rate limit for docs
    if request.url.path in ["/scalar", "/docs", "/openapi.json", "/"]:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    if not RateLimiter.check_rate_limit(client_ip):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, allow all. In prod, specify domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/")
async def root():
    return {"status": "ok", "docs": "/scalar"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
