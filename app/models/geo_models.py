from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

class ObstacleType(str, Enum):
    # Tipos de la API sidewalk
    CURB_RAMP = "CurbRamp"
    NO_CURB_RAMP = "NoCurbRamp"
    OBSTACLE = "Obstacle"
    SURFACE_PROBLEM = "SurfaceProblem"
    NO_SIDEWALK = "NoSidewalk"
    CROSSWALK = "Crosswalk"
    SIGNAL = "Signal"
    OTHER = "Other"
    OCCLUSION = "Occlusion"
    
    # Mapeo a nombres en español (legacy)
    STEP = "escalon"
    POLE = "poste"
    STREET_VENDOR = "comercio_ambulante"
    BROKEN_PAVEMENT = "pavimento_roto"
    TREE = "arbol"
    PARKED_CAR = "auto_estacionado"
    CONSTRUCTION = "construccion"
    NARROW_PATH = "paso_angosto"

class SeverityLevel(str, Enum):
    LOW = "bajo"           # Severidad 1
    MEDIUM = "medio"       # Severidad 2
    HIGH = "alto"          # Severidad 3-4
    CRITICAL = "critico"   # Severidad 5

class Coordinate(BaseModel):
    lat: float = Field(..., description="Latitud")
    lng: float = Field(..., description="Longitud")

class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [lng, lat]

class GeoJSONLineString(BaseModel):
    type: str = "LineString"
    coordinates: List[List[float]]  # [[lng, lat], [lng, lat], ...]

class GeoJSONPolygon(BaseModel):
    type: str = "Polygon"
    coordinates: List[List[List[float]]]  # [[[lng, lat], [lng, lat], ...]]

class Obstacle(BaseModel):
    id: str
    position: Coordinate
    obstacle_type: ObstacleType
    severity: SeverityLevel
    description: Optional[str] = None
    affects_accessibility: bool = True
    
    # Campos adicionales de la API sidewalk
    label_id: Optional[int] = None
    gsv_panorama_id: Optional[str] = None
    label_type_id: Optional[int] = None
    photographer_heading: Optional[float] = None
    heading: Optional[float] = None
    pitch: Optional[float] = None
    zoom: Optional[int] = None
    canvas_x: Optional[int] = None
    canvas_y: Optional[int] = None
    canvas_width: Optional[int] = None
    canvas_height: Optional[int] = None
    severity_value: Optional[int] = None  # 1-5
    temporary: Optional[bool] = None
    tags: Optional[str] = None
    agree_count: Optional[int] = None
    disagree_count: Optional[int] = None
    notsure_count: Optional[int] = None

class SidewalkSegment(BaseModel):
    id: str
    street_name: str
    side: str  # "poniente", "oriente", "norte", "sur"
    start_intersection: str
    end_intersection: str
    geometry: GeoJSONLineString
    length_meters: float
    accessibility_score: float = Field(..., ge=0, le=100)
    obstacles: List[Obstacle] = []
    width_meters: Optional[float] = None
    surface_type: Optional[str] = None  # "concrete", "asphalt", "cobblestone", etc.

class StreetAxis(BaseModel):
    id: str
    name: str
    geometry: GeoJSONLineString
    orientation: str  # "norte_sur", "este_oeste"
    intersections: List[str]  # IDs of intersecting streets
    sidewalk_west: Optional[SidewalkSegment] = None  # poniente
    sidewalk_east: Optional[SidewalkSegment] = None  # oriente
    sidewalk_north: Optional[SidewalkSegment] = None  # norte
    sidewalk_south: Optional[SidewalkSegment] = None  # sur

class CityPolygon(BaseModel):
    city_name: str
    geometry: GeoJSONPolygon
    area_km2: float
    population: Optional[int] = None

class RoutePoint(BaseModel):
    coordinate: Coordinate
    address: Optional[str] = None

class RouteRequest(BaseModel):
    start: RoutePoint
    end: RoutePoint
    accessibility_priority: float = Field(1.0, ge=0, le=1.0, description="0=fastest, 1=most accessible")
    avoid_obstacles: List[ObstacleType] = []

class RouteSegment(BaseModel):
    sidewalk_segment_id: str
    start_coordinate: Coordinate
    end_coordinate: Coordinate
    distance_meters: float
    accessibility_score: float
    estimated_time_seconds: float

class OptimalRoute(BaseModel):
    route_id: str
    segments: List[RouteSegment]
    total_distance_meters: float
    total_time_seconds: float
    average_accessibility_score: float
    geometry: GeoJSONLineString

# Modelos para el mapa de calor de accesibilidad
class SidewalkAccessibility(BaseModel):
    """Vereda con información de accesibilidad para mapa de calor"""
    sidewalk_id: str
    geometry: GeoJSONLineString
    position: Coordinate  # Centro de la vereda
    accessibility_score: float = Field(..., ge=0, le=100, description="Score de accesibilidad (0=inaccesible, 100=perfecto)")
    obstacle_count: int
    obstacles: List[Obstacle]
    severity_breakdown: Dict[str, int] = Field(default_factory=dict, description="Conteo por nivel de severidad")
    
class ObstaclesResponse(BaseModel):
    """Respuesta completa del endpoint de obstáculos"""
    city: str
    total_obstacles: int
    sidewalks: List[SidewalkAccessibility]
    last_updated: Optional[str] = None