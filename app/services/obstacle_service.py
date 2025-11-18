import httpx
from typing import List, Dict, Any, Optional, Tuple
from app.models import (
    Obstacle, ObstacleType, SeverityLevel, Coordinate,
    SidewalkAccessibility, ObstaclesResponse, GeoJSONLineString
)
import math
from datetime import datetime

class ObstacleService:
    """Servicio para obtener y procesar obstáculos de las APIs de sidewalk"""
    
    SIDEWALK_APIS = {
        "santiago": "https://sidewalk-santiago.cs.washington.edu/v3/api/labelClusters?filetype=json",
        "rancagua": "https://sidewalk-rancagua.cs.washington.edu/v3/api/labelClusters?filetype=json"
    }
    
    # Mapeo de label_type_id a ObstacleType
    LABEL_TYPE_MAPPING = {
        1: ObstacleType.CURB_RAMP,
        2: ObstacleType.NO_CURB_RAMP,
        3: ObstacleType.OBSTACLE,
        4: ObstacleType.SURFACE_PROBLEM,
        5: ObstacleType.NO_SIDEWALK,
        6: ObstacleType.CROSSWALK,
        7: ObstacleType.SIGNAL,
        9: ObstacleType.OTHER,
        10: ObstacleType.OCCLUSION
    }
    
    # Pesos de severidad para cálculo de score
    SEVERITY_WEIGHTS = {
        1: 0.2,   # Muy leve
        2: 0.4,   # Leve
        3: 0.6,   # Moderado
        4: 0.8,   # Severo
        5: 1.0    # Muy severo
    }
    
    async def fetch_obstacles(self, city: str) -> List[Dict[str, Any]]:
        """Obtener obstáculos desde la API de sidewalk"""
        city = city.lower()
        if city not in self.SIDEWALK_APIS:
            raise ValueError(f"Ciudad '{city}' no soportada. Ciudades disponibles: {list(self.SIDEWALK_APIS.keys())}")
        
        api_url = self.SIDEWALK_APIS[city]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()
            
        return data.get("features", []) if isinstance(data, dict) else data
    
    def _map_severity(self, severity_value: Optional[int]) -> SeverityLevel:
        """Mapear valor de severidad (1-5) a SeverityLevel"""
        if not severity_value:
            return SeverityLevel.LOW
        
        if severity_value == 1:
            return SeverityLevel.LOW
        elif severity_value == 2:
            return SeverityLevel.MEDIUM
        elif severity_value in [3, 4]:
            return SeverityLevel.HIGH
        else:  # 5
            return SeverityLevel.CRITICAL
    
    def _parse_obstacle(self, feature: Dict[str, Any]) -> Obstacle:
        """Convertir feature de la API a modelo Obstacle"""
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coordinates = geometry.get("coordinates", [0, 0])
        
        # Extraer datos
        label_id = props.get("label_id")
        lat = coordinates[1] if len(coordinates) > 1 else 0
        lng = coordinates[0] if len(coordinates) > 0 else 0
        label_type_id = props.get("label_type_id")
        severity_value = props.get("severity")
        
        # Mapear tipo de obstáculo
        obstacle_type = self.LABEL_TYPE_MAPPING.get(label_type_id, ObstacleType.OTHER)
        severity = self._map_severity(severity_value)
        
        # Determinar si afecta accesibilidad
        affects_accessibility = obstacle_type in [
            ObstacleType.NO_CURB_RAMP,
            ObstacleType.OBSTACLE,
            ObstacleType.SURFACE_PROBLEM,
            ObstacleType.NO_SIDEWALK
        ]
        
        return Obstacle(
            id=f"obs_{label_id}",
            position=Coordinate(lat=lat, lng=lng),
            obstacle_type=obstacle_type,
            severity=severity,
            description=props.get("description"),
            affects_accessibility=affects_accessibility,
            label_id=label_id,
            gsv_panorama_id=props.get("gsv_panorama_id"),
            label_type_id=label_type_id,
            photographer_heading=props.get("photographer_heading"),
            heading=props.get("heading"),
            pitch=props.get("pitch"),
            zoom=props.get("zoom"),
            canvas_x=props.get("canvas_x"),
            canvas_y=props.get("canvas_y"),
            canvas_width=props.get("canvas_width"),
            canvas_height=props.get("canvas_height"),
            severity_value=severity_value,
            temporary=props.get("temporary"),
            tags=props.get("tags"),
            agree_count=props.get("agree_count"),
            disagree_count=props.get("disagree_count"),
            notsure_count=props.get("notsure_count")
        )
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcular distancia en metros entre dos coordenadas usando fórmula de Haversine"""
        R = 6371000  # Radio de la Tierra en metros
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _find_nearest_point_on_line(self, point: Coordinate, line_coords: List[List[float]]) -> Tuple[Coordinate, float]:
        """
        Encontrar el punto más cercano en una línea (vereda) a un punto dado (obstáculo)
        Retorna: (punto_más_cercano, distancia_mínima)
        """
        min_distance = float('inf')
        nearest_point = None
        
        # Revisar cada segmento de la línea
        for i in range(len(line_coords) - 1):
            p1_lng, p1_lat = line_coords[i]
            p2_lng, p2_lat = line_coords[i + 1]
            
            # Calcular distancia al punto medio del segmento (simplificación)
            mid_lat = (p1_lat + p2_lat) / 2
            mid_lng = (p1_lng + p2_lng) / 2
            
            distance = self._haversine_distance(point.lat, point.lng, mid_lat, mid_lng)
            
            if distance < min_distance:
                min_distance = distance
                nearest_point = Coordinate(lat=mid_lat, lng=mid_lng)
        
        return nearest_point, min_distance
    
    def _associate_obstacles_to_sidewalks(
        self, 
        obstacles: List[Obstacle], 
        sidewalk_geometries: List[Dict[str, Any]],
        max_distance_meters: float = 50.0
    ) -> Dict[str, List[Obstacle]]:
        """
        Asociar cada obstáculo a la vereda más cercana
        
        Args:
            obstacles: Lista de obstáculos
            sidewalk_geometries: Lista de diccionarios con {id, geometry}
            max_distance_meters: Distancia máxima para asociar un obstáculo a una vereda
            
        Returns:
            Diccionario {sidewalk_id: [obstáculos]}
        """
        sidewalk_obstacles: Dict[str, List[Obstacle]] = {
            sw["id"]: [] for sw in sidewalk_geometries
        }
        
        for obstacle in obstacles:
            if not obstacle.affects_accessibility:
                continue
                
            min_distance = float('inf')
            nearest_sidewalk_id = None
            
            # Encontrar la vereda más cercana
            for sidewalk in sidewalk_geometries:
                line_coords = sidewalk["geometry"].coordinates
                _, distance = self._find_nearest_point_on_line(obstacle.position, line_coords)
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_sidewalk_id = sidewalk["id"]
            
            # Asociar si está dentro del rango
            if nearest_sidewalk_id and min_distance <= max_distance_meters:
                sidewalk_obstacles[nearest_sidewalk_id].append(obstacle)
        
        return sidewalk_obstacles
    
    def _calculate_accessibility_score(self, obstacles: List[Obstacle]) -> float:
        """
        Calcular score de accesibilidad basado en obstáculos (0-100)
        100 = perfecto (sin obstáculos)
        0 = muy inaccesible
        """
        if not obstacles:
            return 100.0
        
        # Calcular penalización total
        total_penalty = 0.0
        for obs in obstacles:
            severity_weight = self.SEVERITY_WEIGHTS.get(obs.severity_value or 3, 0.6)
            total_penalty += severity_weight * 10  # Cada obstáculo puede restar hasta 10 puntos según severidad
        
        # Calcular score (mínimo 0)
        score = max(0.0, 100.0 - total_penalty)
        return round(score, 2)
    
    def _get_severity_breakdown(self, obstacles: List[Obstacle]) -> Dict[str, int]:
        """Obtener conteo de obstáculos por nivel de severidad"""
        breakdown = {
            "bajo": 0,
            "medio": 0,
            "alto": 0,
            "critico": 0
        }
        
        for obs in obstacles:
            severity_key = obs.severity.value
            if severity_key in breakdown:
                breakdown[severity_key] += 1
        
        return breakdown
    
    async def get_obstacles_with_sidewalks(
        self, 
        city: str,
        sidewalk_geometries: Optional[List[Dict[str, Any]]] = None
    ) -> ObstaclesResponse:
        """
        Obtener obstáculos asociados a veredas con scores de accesibilidad
        
        Args:
            city: Nombre de la ciudad
            sidewalk_geometries: Lista opcional de geometrías de veredas.
                                 Si no se proporciona, se generará una cuadrícula básica.
        """
        # Obtener obstáculos de la API
        features = await self.fetch_obstacles(city)
        obstacles = [self._parse_obstacle(f) for f in features]
        
        # Si no se proporcionan geometrías de veredas, crear una cuadrícula básica
        if not sidewalk_geometries:
            sidewalk_geometries = self._generate_default_sidewalk_grid(obstacles)
        
        # Asociar obstáculos a veredas
        sidewalk_obstacles = self._associate_obstacles_to_sidewalks(obstacles, sidewalk_geometries)
        
        # Crear respuesta con scores de accesibilidad
        sidewalks_accessibility = []
        for sidewalk in sidewalk_geometries:
            sidewalk_id = sidewalk["id"]
            geometry = sidewalk["geometry"]
            obs_list = sidewalk_obstacles.get(sidewalk_id, [])
            
            # Calcular centro de la vereda
            coords = geometry.coordinates
            if coords:
                center_lat = sum(c[1] for c in coords) / len(coords)
                center_lng = sum(c[0] for c in coords) / len(coords)
            else:
                center_lat, center_lng = 0, 0
            
            sidewalk_acc = SidewalkAccessibility(
                sidewalk_id=sidewalk_id,
                geometry=geometry,
                position=Coordinate(lat=center_lat, lng=center_lng),
                accessibility_score=self._calculate_accessibility_score(obs_list),
                obstacle_count=len(obs_list),
                obstacles=obs_list,
                severity_breakdown=self._get_severity_breakdown(obs_list)
            )
            sidewalks_accessibility.append(sidewalk_acc)
        
        return ObstaclesResponse(
            city=city,
            total_obstacles=len(obstacles),
            sidewalks=sidewalks_accessibility,
            last_updated=datetime.utcnow().isoformat()
        )
    
    def _generate_default_sidewalk_grid(self, obstacles: List[Obstacle]) -> List[Dict[str, Any]]:
        """
        Generar cuadrícula de veredas cuando no se proporcionan geometrías reales
        Divide el área en celdas de aproximadamente 100x100 metros
        """
        if not obstacles:
            return []
        
        # Encontrar bounding box de los obstáculos
        lats = [obs.position.lat for obs in obstacles]
        lngs = [obs.position.lng for obs in obstacles]
        
        min_lat, max_lat = min(lats), max(lats)
        min_lng, max_lng = min(lngs), max(lngs)
        
        # Crear celdas de aproximadamente 100x100 metros
        # 1 grado ≈ 111km, entonces 0.001 grados ≈ 111 metros
        cell_size = 0.001  # aproximadamente 100 metros
        
        sidewalks = []
        lat = min_lat
        cell_id = 0
        
        while lat < max_lat:
            lng = min_lng
            while lng < max_lng:
                # Crear línea de vereda (celda)
                coords = [
                    [lng, lat],
                    [lng + cell_size, lat],
                    [lng + cell_size, lat + cell_size],
                    [lng, lat + cell_size],
                    [lng, lat]
                ]
                
                sidewalks.append({
                    "id": f"sidewalk_{cell_id}",
                    "geometry": GeoJSONLineString(
                        type="LineString",
                        coordinates=coords
                    )
                })
                
                cell_id += 1
                lng += cell_size
            lat += cell_size
        
        return sidewalks
