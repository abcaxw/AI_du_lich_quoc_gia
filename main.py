# app/main.py
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

import dconfig
import dlog
from database import milvus_service, mysql_service, minio_service
from routes import (
    health_route,
    chat_route,
    meta_route,
    destination_route,
    tour_route,
    booking_route
)

app = FastAPI(title="Tourism AI Assistant")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/web/templates")

# Create necessary directories
try:
    os.makedirs(dconfig.config_object.LOG_DIR, exist_ok=True)
    os.makedirs(os.path.join(dconfig.config_object.DATA_DIR, 'temp'), exist_ok=True)
except OSError:
    pass

@app.on_event("shutdown")
def shutdown_event():
    milvus_service.disconnect()
    mysql_service.disconnect()
    minio_service.disconnect()

@app.get("/")
async def root():
    return {"message": "Tourism AI Assistant API"}

# Include routers
app.include_router(health_route.router)
app.include_router(chat_route.router)
app.include_router(meta_route.router)
app.include_router(destination_route.router)
app.include_router(tour_route.router)
app.include_router(booking_route.router)

if __name__ == '__main__':
    dlog.dlog_i(f"Server started at {dconfig.config_object.SERVER_NAME}:{dconfig.config_object.PORT_NUMBER}")
    uvicorn.run(
        app,
        host=dconfig.config_object.SERVER_NAME,
        port=int(dconfig.config_object.PORT_NUMBER),
        proxy_headers=True
    )