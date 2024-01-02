from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from home import router as home_route
from uploads import router as upload_route

# Configurar middleware CORS en la misma instancia de FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_route)
app.include_router(home_route)

if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)