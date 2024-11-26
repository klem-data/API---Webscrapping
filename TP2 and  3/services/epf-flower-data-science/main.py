from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.app import get_application
from api.routes import data

app = get_application()

# Inclusion des routes
app.include_router(data.router, prefix="/api")

# Redirect root endpoint to Swagger documentation
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", debug=True, reload=True, port=8080)
