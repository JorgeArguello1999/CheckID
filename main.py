from fastapi import FastAPI

from home import router as home_route
from uploads import router as upload_route

app = FastAPI()

app.include_router(upload_route)
app.include_router(home_route)

if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)