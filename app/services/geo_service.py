import math
from typing import List, Optional, Tuple, Dict, Any
from app.models import (
    CityPolygon, StreetAxis, SidewalkSegment, RouteRequest, 
    OptimalRoute, Coordinate, GeoJSONLineString, Obstacle,
    ObstacleType, SeverityLevel, RouteSegment
)
from app.data.mock_data import get_mock_data
import uuid
import heapq

class GeoService:
    def __init__(self):
        self.mock_data = get_mock_data()
    
    def get_available_cities(self) -> List[str]:
        """Obtener ciudades disponibles"""
        return list(self.mock_data.keys())
    
    def get_city_polygon(self, city: str) -> CityPolygon:
        """Obtener polígono de límites de la ciudad"""
        city = city.lower()
        if city not in self.mock_data:
            raise ValueError(f"Ciudad '{city}' no encontrada")
        
        return self.mock_data[city]["polygon"]
    
    def get_street_network(self, city: str, bbox: Optional[List[float]] = None, limit: int = 100) -> List[StreetAxis]:
        """Obtener red de calles con filtros opcionales"""
        city = city.lower()
        if city not in self.mock_data:
            raise ValueError(f"Ciudad '{city}' no encontrada")
        
        streets = self.mock_data[city]["streets"]
        
        # Aplicar filtro de bounding box si se proporciona
        if bbox:
            min_lng, min_lat, max_lng, max_lat = bbox
            filtered_streets = []
            
            for street in streets:
                # Verificar si la calle intersecta con el bbox
                if self._street_intersects_bbox(street, min_lng, min_lat, max_lng, max_lat):
                    filtered_streets.append(street)
            
            streets = filtered_streets
        
        # Aplicar límite
        return streets[:limit]
    
    def get_sidewalk_segments(self, city: str, street_name: Optional[str] = None, 
                            min_accessibility_score: float = 0, 
                            bbox: Optional[List[float]] = None) -> List[SidewalkSegment]:
        """Obtener segmentos de veredas con filtros"""
        city = city.lower()
        if city not in self.mock_data:
            raise ValueError(f"Ciudad '{city}' no encontrada")
        
        # Obtener todos los segmentos de veredas de todas las calles
        segments = []
        for street in self.mock_data[city]["streets"]:
            # Filtrar por nombre de calle si se especifica
            if street_name and street_name.lower() not in street.name.lower():
                continue
            
            # Agregar segmentos de veredas de esta calle
            if street.sidewalk_west:
                segments.append(street.sidewalk_west)
            if street.sidewalk_east:
                segments.append(street.sidewalk_east)
            if street.sidewalk_north:
                segments.append(street.sidewalk_north)
            if street.sidewalk_south:
                segments.append(street.sidewalk_south)
        
        # Filtrar por score de accesibilidad
        segments = [s for s in segments if s and s.accessibility_score >= min_accessibility_score]
        
        # Filtrar por bbox si se proporciona
        if bbox:
            min_lng, min_lat, max_lng, max_lat = bbox
            filtered_segments = []
            
            for segment in segments:
                if self._segment_intersects_bbox(segment, min_lng, min_lat, max_lng, max_lat):
                    filtered_segments.append(segment)
            
            segments = filtered_segments
        
        return segments
    
    def get_street_sidewalk_segments(self, city: str, street_id: str) -> List[SidewalkSegment]:
        """Obtener segmentos de vereda de una calle específica"""
        city = city.lower()
        if city not in self.mock_data:
            raise ValueError(f"Ciudad '{city}' no encontrada")
        
        # Buscar la calle por ID
        street = None
        for s in self.mock_data[city]["streets"]:
            if s.id == street_id:
                street = s
                break
        
        if not street:
            raise ValueError(f"Calle con ID '{street_id}' no encontrada")
        
        # Recopilar todos los segmentos de veredas
        segments = []
        if street.sidewalk_west:
            segments.append(street.sidewalk_west)
        if street.sidewalk_east:
            segments.append(street.sidewalk_east)
        if street.sidewalk_north:
            segments.append(street.sidewalk_north)
        if street.sidewalk_south:
            segments.append(street.sidewalk_south)
        
        return segments
    
    def calculate_optimal_route(self, city: str, route_request: RouteRequest) -> OptimalRoute:
        """Calcular ruta óptima usando algoritmo de pathfinding"""
        city = city.lower()
        if city not in self.mock_data:
            raise ValueError(f"Ciudad '{city}' no encontrada")
        
        # Obtener todos los segmentos de veredas
        segments = self.get_sidewalk_segments(city)
        
        # Encontrar segmentos más cercanos al punto de inicio y fin
        start_segment = self._find_nearest_segment(route_request.start.coordinate, segments)
        end_segment = self._find_nearest_segment(route_request.end.coordinate, segments)
        
        if not start_segment or not end_segment:
            raise ValueError("No se pudo encontrar segmentos de veredas cerca de los puntos especificados")
        
        # Usar algoritmo A* para encontrar la ruta óptima
        route_segments = self._find_path_astar(
            start_segment, 
            end_segment, 
            segments, 
            route_request.accessibility_priority,
            route_request.avoid_obstacles
        )
        
        # Calcular métricas de la ruta
        total_distance = sum(seg.distance_meters for seg in route_segments)
        total_time = sum(seg.estimated_time_seconds for seg in route_segments)
        avg_accessibility = sum(seg.accessibility_score for seg in route_segments) / len(route_segments) if route_segments else 0
        
        # Generar geometría de la ruta completa
        route_coordinates = []
        for segment in route_segments:
            route_coordinates.extend([
                [segment.start_coordinate.lng, segment.start_coordinate.lat],
                [segment.end_coordinate.lng, segment.end_coordinate.lat]
            ])
        
        return OptimalRoute(
            route_id=str(uuid.uuid4()),
            segments=route_segments,
            total_distance_meters=total_distance,
            total_time_seconds=total_time,
            average_accessibility_score=avg_accessibility,
            geometry=GeoJSONLineString(coordinates=route_coordinates)
        )
    
    def _street_intersects_bbox(self, street: StreetAxis, min_lng: float, min_lat: float, 
                              max_lng: float, max_lat: float) -> bool:
        """Verificar si una calle intersecta con un bounding box"""
        for coord in street.geometry.coordinates:
            lng, lat = coord[0], coord[1]
            if min_lng <= lng <= max_lng and min_lat <= lat <= max_lat:
                return True
        return False
    
    def _segment_intersects_bbox(self, segment: SidewalkSegment, min_lng: float, min_lat: float,
                               max_lng: float, max_lat: float) -> bool:
        """Verificar si un segmento de vereda intersecta con un bounding box"""
        for coord in segment.geometry.coordinates:
            lng, lat = coord[0], coord[1]
            if min_lng <= lng <= max_lng and min_lat <= lat <= max_lat:
                return True
        return False
    
    def _find_nearest_segment(self, point: Coordinate, segments: List[SidewalkSegment]) -> Optional[SidewalkSegment]:
        """Encontrar el segmento de vereda más cercano a un punto"""
        min_distance = float('inf')
        nearest_segment = None
        
        for segment in segments:
            # Calcular distancia al punto medio del segmento
            coords = segment.geometry.coordinates
            if len(coords) >= 2:
                mid_lng = (coords[0][0] + coords[-1][0]) / 2
                mid_lat = (coords[0][1] + coords[-1][1]) / 2
                
                distance = self._calculate_distance(
                    point.lat, point.lng,
                    mid_lat, mid_lng
                )
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_segment = segment
        
        return nearest_segment
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calcular distancia entre dos puntos usando fórmula de Haversine"""
        R = 6371000  # Radio de la Tierra en metros
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _find_path_astar(self, start: SidewalkSegment, end: SidewalkSegment,
                        all_segments: List[SidewalkSegment], accessibility_priority: float,
                        avoid_obstacles: List[ObstacleType]) -> List[RouteSegment]:
        """Algoritmo A* para encontrar ruta óptima"""
        # Implementación simplificada - en producción usaríamos una librería como NetworkX
        
        # Por ahora, retornar ruta directa usando los segmentos más accesibles
        # En una implementación completa, construiríamos un grafo de conectividad
        
        route_segments = []
        
        # Crear segmento de ruta para el segmento de inicio
        start_coords = start.geometry.coordinates
        start_coord = Coordinate(lat=start_coords[0][1], lng=start_coords[0][0])
        end_coord = Coordinate(lat=start_coords[-1][1], lng=start_coords[-1][0])
        
        # Calcular penalización por obstáculos
        obstacle_penalty = 0
        for obstacle in start.obstacles:
            if obstacle.obstacle_type in avoid_obstacles:
                obstacle_penalty += 20  # Penalización por obstáculo a evitar
            obstacle_penalty += {"bajo": 5, "medio": 15, "alto": 30, "critico": 50}[obstacle.severity.value]
        
        accessibility_score = max(0, start.accessibility_score - obstacle_penalty)
        
        # Estimar tiempo basado en accesibilidad y velocidad de caminata
        base_speed_mps = 1.4  # 1.4 m/s velocidad promedio caminando
        accessibility_factor = accessibility_score / 100
        adjusted_speed = base_speed_mps * (0.5 + 0.5 * accessibility_factor)  # 0.5-1.0 factor
        
        route_segment = RouteSegment(
            sidewalk_segment_id=start.id,
            start_coordinate=start_coord,
            end_coordinate=end_coord,
            distance_meters=start.length_meters,
            accessibility_score=accessibility_score,
            estimated_time_seconds=start.length_meters / adjusted_speed
        )
        
        route_segments.append(route_segment)
        
        return route_segments