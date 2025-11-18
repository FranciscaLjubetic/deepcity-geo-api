from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json
import os
from app.routers import geo_router

app = FastAPI(
    title="DeepCity Geo API",
    description="API para datos geoespaciales de calles, veredas y rutas accesibles para ciudades chilenas",
    version="1.0.0"
)

# Montar archivos estáticos
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Configurar CORS para permitir requests desde Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(geo_router)

@app.get("/")
async def root():
    return {
        "message": "DeepCity Geo API - Datos geoespaciales para accesibilidad urbana",
        "cities": ["santiago", "rancagua"],
        "endpoints": {
            "city_polygons": "/api/v1/cities/{city}/polygons",
            "street_network": "/api/v1/cities/{city}/streets",
            "sidewalk_segments": "/api/v1/cities/{city}/sidewalks",
            "optimal_route": "/api/v1/cities/{city}/route"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "deepcity-geo-api"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Servir el favicon"""
    # Intentar primero con .ico
    favicon_ico = os.path.join(static_path, "favicon.ico")
    if os.path.exists(favicon_ico):
        return FileResponse(favicon_ico, media_type="image/x-icon")
    
    # Si no existe, usar SVG
    favicon_svg = os.path.join(static_path, "favicon.svg")
    if os.path.exists(favicon_svg):
        return FileResponse(favicon_svg, media_type="image/svg+xml")
    
    # Si no hay ninguno, retornar 404
    raise HTTPException(status_code=404, detail="Favicon not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)