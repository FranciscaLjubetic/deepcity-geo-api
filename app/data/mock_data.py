from typing import Dict, Any
from app.models import (
    CityPolygon, StreetAxis, SidewalkSegment, Obstacle, 
    GeoJSONPolygon, GeoJSONLineString, Coordinate,
    ObstacleType, SeverityLevel
)

def get_mock_data() -> Dict[str, Any]:
    """Datos mock para Santiago y Rancagua"""
    
    # Datos para Santiago
    santiago_polygon = CityPolygon(
        city_name="Santiago",
        geometry=GeoJSONPolygon(coordinates=[[
            [-70.7500, -33.5500],  # Noroeste
            [-70.4500, -33.5500],  # Noreste
            [-70.4500, -33.7500],  # Sureste
            [-70.7500, -33.7500],  # Suroeste
            [-70.7500, -33.5500]   # Cierre
        ]]),
        area_km2=641.4,
        population=7112808
    )
    
    # Calles principales de Santiago
    santiago_streets = [
        StreetAxis(
            id="stgo_alameda",
            name="Avenida Libertador Bernardo O'Higgins",
            geometry=GeoJSONLineString(coordinates=[
                [-70.7000, -33.4400],
                [-70.6500, -33.4410],
                [-70.6000, -33.4420],
                [-70.5500, -33.4430]
            ]),
            orientation="este_oeste",
            intersections=["stgo_estado", "stgo_bandera", "stgo_ahumada"],
            sidewalk_north=SidewalkSegment(
                id="alameda_norte_1",
                street_name="Avenida Libertador Bernardo O'Higgins",
                side="norte",
                start_intersection="Plaza Baquedano",
                end_intersection="Plaza de Armas",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.7000, -33.4395],
                    [-70.5500, -33.4425]
                ]),
                length_meters=1200,
                accessibility_score=75.0,
                width_meters=3.5,
                surface_type="concrete",
                obstacles=[
                    Obstacle(
                        id="obs_alameda_1",
                        position=Coordinate(lat=-33.4400, lng=-70.6500),
                        obstacle_type=ObstacleType.POLE,
                        severity=SeverityLevel.LOW,
                        description="Poste de señalización"
                    )
                ]
            ),
            sidewalk_south=SidewalkSegment(
                id="alameda_sur_1",
                street_name="Avenida Libertador Bernardo O'Higgins",
                side="sur",
                start_intersection="Plaza Baquedano",
                end_intersection="Plaza de Armas",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.7000, -33.4405],
                    [-70.5500, -33.4435]
                ]),
                length_meters=1200,
                accessibility_score=65.0,
                width_meters=2.8,
                surface_type="concrete",
                obstacles=[
                    Obstacle(
                        id="obs_alameda_2",
                        position=Coordinate(lat=-33.4410, lng=-70.6200),
                        obstacle_type=ObstacleType.STREET_VENDOR,
                        severity=SeverityLevel.MEDIUM,
                        description="Puesto ambulante"
                    ),
                    Obstacle(
                        id="obs_alameda_3",
                        position=Coordinate(lat=-33.4415, lng=-70.5800),
                        obstacle_type=ObstacleType.STEP,
                        severity=SeverityLevel.HIGH,
                        description="Escalón de 15cm"
                    )
                ]
            )
        ),
        StreetAxis(
            id="stgo_estado",
            name="Calle Estado",
            geometry=GeoJSONLineString(coordinates=[
                [-70.6500, -33.4200],
                [-70.6500, -33.4600]
            ]),
            orientation="norte_sur",
            intersections=["stgo_alameda", "stgo_moneda"],
            sidewalk_west=SidewalkSegment(
                id="estado_poniente_1",
                street_name="Calle Estado",
                side="poniente",
                start_intersection="Moneda",
                end_intersection="Compañía",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.6505, -33.4200],
                    [-70.6505, -33.4600]
                ]),
                length_meters=800,
                accessibility_score=85.0,
                width_meters=4.0,
                surface_type="concrete"
            ),
            sidewalk_east=SidewalkSegment(
                id="estado_oriente_1",
                street_name="Calle Estado",
                side="oriente",
                start_intersection="Moneda",
                end_intersection="Compañía",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.6495, -33.4200],
                    [-70.6495, -33.4600]
                ]),
                length_meters=800,
                accessibility_score=70.0,
                width_meters=3.2,
                surface_type="concrete",
                obstacles=[
                    Obstacle(
                        id="obs_estado_1",
                        position=Coordinate(lat=-33.4350, lng=-70.6495),
                        obstacle_type=ObstacleType.TREE,
                        severity=SeverityLevel.LOW,
                        description="Árbol en vereda"
                    )
                ]
            )
        )
    ]
    
    # Datos para Rancagua
    rancagua_polygon = CityPolygon(
        city_name="Rancagua",
        geometry=GeoJSONPolygon(coordinates=[[
            [-70.7800, -34.1400],  # Noroeste
            [-70.7200, -34.1400],  # Noreste
            [-70.7200, -34.1800],  # Sureste
            [-70.7800, -34.1800],  # Suroeste
            [-70.7800, -34.1400]   # Cierre
        ]]),
        area_km2=260.3,
        population=241774
    )
    
    # Calles principales de Rancagua
    rancagua_streets = [
        StreetAxis(
            id="rga_independencia",
            name="Paseo Independencia",
            geometry=GeoJSONLineString(coordinates=[
                [-70.7600, -34.1600],
                [-70.7400, -34.1600],
                [-70.7200, -34.1600]
            ]),
            orientation="este_oeste",
            intersections=["rga_estado", "rga_millán"],
            sidewalk_north=SidewalkSegment(
                id="independencia_norte_1",
                street_name="Paseo Independencia",
                side="norte",
                start_intersection="Estado",
                end_intersection="Millán",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.7600, -34.1595],
                    [-70.7200, -34.1595]
                ]),
                length_meters=400,
                accessibility_score=90.0,
                width_meters=5.0,
                surface_type="concrete"
            ),
            sidewalk_south=SidewalkSegment(
                id="independencia_sur_1",
                street_name="Paseo Independencia",
                side="sur",
                start_intersection="Estado",
                end_intersection="Millán",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.7600, -34.1605],
                    [-70.7200, -34.1605]
                ]),
                length_meters=400,
                accessibility_score=88.0,
                width_meters=4.8,
                surface_type="concrete",
                obstacles=[
                    Obstacle(
                        id="obs_independencia_1",
                        position=Coordinate(lat=-34.1605, lng=-70.7400),
                        obstacle_type=ObstacleType.POLE,
                        severity=SeverityLevel.LOW,
                        description="Poste de alumbrado"
                    )
                ]
            )
        ),
        StreetAxis(
            id="rga_estado_rancagua",
            name="Calle Estado",
            geometry=GeoJSONLineString(coordinates=[
                [-70.7500, -34.1500],
                [-70.7500, -34.1700]
            ]),
            orientation="norte_sur",
            intersections=["rga_independencia", "rga_san_martin"],
            sidewalk_west=SidewalkSegment(
                id="estado_rga_poniente_1",
                street_name="Calle Estado",
                side="poniente",
                start_intersection="Independencia",
                end_intersection="San Martín",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.7505, -34.1500],
                    [-70.7505, -34.1700]
                ]),
                length_meters=300,
                accessibility_score=80.0,
                width_meters=3.0,
                surface_type="concrete"
            ),
            sidewalk_east=SidewalkSegment(
                id="estado_rga_oriente_1",
                street_name="Calle Estado",
                side="oriente",
                start_intersection="Independencia",
                end_intersection="San Martín",
                geometry=GeoJSONLineString(coordinates=[
                    [-70.7495, -34.1500],
                    [-70.7495, -34.1700]
                ]),
                length_meters=300,
                accessibility_score=75.0,
                width_meters=2.8,
                surface_type="concrete",
                obstacles=[
                    Obstacle(
                        id="obs_estado_rga_1",
                        position=Coordinate(lat=-34.1600, lng=-70.7495),
                        obstacle_type=ObstacleType.BROKEN_PAVEMENT,
                        severity=SeverityLevel.MEDIUM,
                        description="Pavimento agrietado"
                    )
                ]
            )
        )
    ]
    
    return {
        "santiago": {
            "polygon": santiago_polygon,
            "streets": santiago_streets
        },
        "rancagua": {
            "polygon": rancagua_polygon,
            "streets": rancagua_streets
        }
    }