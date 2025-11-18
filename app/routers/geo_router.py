from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from app.models import CityPolygon, StreetAxis, SidewalkSegment, RouteRequest, OptimalRoute, ObstaclesResponse
from app.services.geo_service import GeoService
from app.services.obstacle_service import ObstacleService

router = APIRouter(prefix="/api/v1", tags=["Geospatial Data"])

geo_service = GeoService()
obstacle_service = ObstacleService()

@router.get("/cities", response_model=List[str])
async def get_available_cities():
    """Obtener lista de ciudades disponibles"""
    return geo_service.get_available_cities()

@router.get("/cities/{city}/polygons", response_model=CityPolygon)
async def get_city_polygons(
    city: str = Path(..., description="Nombre de la ciudad (santiago, rancagua)")
):
    """Obtener polígonos de límites de la ciudad"""
    try:
        return geo_service.get_city_polygon(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/cities/{city}/streets", response_model=List[StreetAxis])
async def get_street_network(
    city: str = Path(..., description="Nombre de la ciudad"),
    bbox: Optional[str] = Query(None, description="Bounding box: 'min_lng,min_lat,max_lng,max_lat'"),
    limit: Optional[int] = Query(100, description="Número máximo de calles a retornar")
):
    """Obtener red de calles con ejes y veredas"""
    try:
        bbox_coords = None
        if bbox:
            coords = [float(x) for x in bbox.split(',')]
            if len(coords) != 4:
                raise HTTPException(status_code=400, detail="Bbox debe tener formato: min_lng,min_lat,max_lng,max_lat")
            bbox_coords = coords
        
        return geo_service.get_street_network(city, bbox_coords, limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/cities/{city}/sidewalks", response_model=List[SidewalkSegment])
async def get_sidewalk_segments(
    city: str = Path(..., description="Nombre de la ciudad"),
    street_name: Optional[str] = Query(None, description="Filtrar por nombre de calle"),
    min_accessibility_score: Optional[float] = Query(0, ge=0, le=100, description="Score mínimo de accesibilidad"),
    bbox: Optional[str] = Query(None, description="Bounding box: 'min_lng,min_lat,max_lng,max_lat'")
):
    """Obtener segmentos de veredas con información de accesibilidad"""
    try:
        bbox_coords = None
        if bbox:
            coords = [float(x) for x in bbox.split(',')]
            if len(coords) != 4:
                raise HTTPException(status_code=400, detail="Bbox debe tener formato: min_lng,min_lat,max_lng,max_lat")
            bbox_coords = coords
            
        return geo_service.get_sidewalk_segments(
            city, 
            street_name=street_name,
            min_accessibility_score=min_accessibility_score,
            bbox=bbox_coords
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/cities/{city}/route", response_model=OptimalRoute)
async def calculate_optimal_route(
    city: str = Path(..., description="Nombre de la ciudad"),
    route_request: RouteRequest = ...
):
    """Calcular ruta óptima entre dos puntos considerando accesibilidad"""
    try:
        return geo_service.calculate_optimal_route(city, route_request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando ruta: {str(e)}")

@router.get("/cities/{city}/streets/{street_id}/segments", response_model=List[SidewalkSegment])
async def get_street_sidewalk_segments(
    city: str = Path(..., description="Nombre de la ciudad"),
    street_id: str = Path(..., description="ID de la calle")
):
    """Obtener segmentos de vereda de una calle específica"""
    try:
        return geo_service.get_street_sidewalk_segments(city, street_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/cities/{city}/obstacles", response_model=ObstaclesResponse)
async def get_obstacles_with_accessibility(
    city: str = Path(..., description="Nombre de la ciudad (santiago, rancagua)")
):
    """
    Obtener obstáculos asociados a veredas con scores de accesibilidad
    
    Este endpoint consume las APIs de sidewalk-santiago/rancagua, procesa los obstáculos
    y los asocia a veredas, calculando un score de accesibilidad (0-100) para cada vereda.
    
    **Score de accesibilidad:**
    - 100: Perfectamente accesible (sin obstáculos)
    - 75-99: Buena accesibilidad (obstáculos menores)
    - 50-74: Accesibilidad moderada
    - 25-49: Baja accesibilidad
    - 0-24: Muy inaccesible
    
    **Uso para mapa de calor:**
    Los datos retornados están listos para crear un mapa de calor:
    - `accessibility_score`: Usar para el color del mapa (verde=100, rojo=0)
    - `geometry`: Coordenadas de la vereda para dibujar en el mapa
    - `obstacles`: Lista detallada de obstáculos en cada vereda
    - `severity_breakdown`: Distribución de obstáculos por severidad
    """
    try:
        # Obtener geometrías de veredas reales si están disponibles
        # Por ahora usamos una cuadrícula automática
        return await obstacle_service.get_obstacles_with_sidewalks(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo obstáculos: {str(e)}")