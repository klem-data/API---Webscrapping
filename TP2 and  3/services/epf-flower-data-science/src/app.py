from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from src.api.router import router
from firebase_admin import auth
from fastapi.responses import JSONResponse
import redis
import time


# Rate limiter class implementation
class RateLimiter:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.rate_limit = 100  # requests
        self.time_window = 60  # seconds

    async def check_rate_limit(self, user_id: str):
        current = int(time.time())
        key = f"rate_limit:{user_id}:{current // self.time_window}"
        
        count = self.redis_client.incr(key)
        if count == 1:
            self.redis_client.expire(key, self.time_window)
        
        if count > self.rate_limit:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

def get_application() -> FastAPI:
    app = FastAPI(
        title="EPF Flower Data Science",
        description="EPF Flower Data Science for DAIPA Blandine",
        version="1.0",
    )

    # Configure CORS with authorized domains from Firebase
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "localhost",
            "myproject-0412025-94c7f.firebaseapp.com",
            "myproject-0412025-94c7f.web.app",
            "0.0.0.0"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add rate limiting middleware
    rate_limiter = RateLimiter()

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        if token := request.headers.get("Authorization"):
            try:
                user = auth.verify_id_token(token.split(" ")[1])
                await rate_limiter.check_rate_limit(user["uid"])
            except Exception as e:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authentication credentials"}
                )
        response = await call_next(request)
        return response

    # Add custom error handlers
    @app.exception_handler(404)
    async def custom_404_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Resource not found. Please check the URL and try again.",
                "path": str(request.url),
                "app_name": "EPF Flower Data Science for DAIPA Blandine"
            }
        )

    # Add validation error handler
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=422,
            content={
                "message": "Validation error in request",
                "details": str(exc)
            }
        )

    # Include routers with version prefix
    app.include_router(router, prefix="/v1")

    return app

# Create application instance
app = get_application()
