# DeepCity Geo API

API FastAPI para servir datos geoespaciales de calles, veredas y rutas accesibles para ciudades chilenas.

## Características

- **Polígonos de ciudad**: Límites geográficos de Santiago y Rancagua
- **Red de calles**: Ejes viales con información de orientación
- **Segmentación de veredas**: División automática de veredas por intersecciones
- **Evaluación de accesibilidad**: Sistema de scoring para obstáculos
- **Cálculo de rutas óptimas**: Algoritmo de pathfinding para rutas accesibles

## Estructura del Proyecto

```
deepcity-geo-api/
├── main.py              # Aplicación FastAPI principal
├── requirements.txt     # Dependencias Python
├── vercel.json          # Configuración para Vercel
├── app/
│   ├── models/          # Modelos Pydantic
│   ├── routers/         # Endpoints de la API
│   ├── services/        # Lógica de negocio
│   └── data/           # Datos mock y reales
└── README.md           # Este archivo
```

## Instalación y Uso

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
python main.py

# Acceder a la API en: http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

### Deploy en Vercel

```bash
vercel --prod
```

## Endpoints

### Ciudades Disponibles
- `GET /` - Información general y endpoints disponibles
- `GET /health` - Health check

### Datos Geoespaciales
- `GET /api/v1/cities/{city}/polygons` - Polígonos de la ciudad
- `GET /api/v1/cities/{city}/streets` - Red de calles con ejes
- `GET /api/v1/cities/{city}/sidewalks` - Veredas segmentadas
- `GET /api/v1/cities/{city}/obstacles` - **Obstáculos con scores de accesibilidad para mapa de calor**
- `POST /api/v1/cities/{city}/route` - Calcular ruta óptima

### Ciudades Soportadas
- `santiago` - Santiago de Chile
- `rancagua` - Rancagua, VI Región

## Modelo de Datos

### Street (Calle)
- Eje principal con orientación norte-sur o este-oeste
- Veredas asociadas (poniente/oriente o norte/sur)
- Intersecciones con otras calles

### Sidewalk Segment (Segmento de Vereda)
- Tramo de vereda entre intersecciones
- Score de accesibilidad (0-100)
- Lista de obstáculos detectados

### Obstacle (Obstáculo)
- Posición geográfica
- Tipo (escalón, poste, comercio ambulante, etc.)
- Severidad (bajo, medio, alto)

## Mapa de Calor de Accesibilidad

El endpoint `/api/v1/cities/{city}/obstacles` está diseñado específicamente para crear mapas de calor:

### Características
- **Consume APIs reales**: Datos de sidewalk-santiago.cs.washington.edu y sidewalk-rancagua.cs.washington.edu
- **Asociación inteligente**: Cada obstáculo se asocia a la vereda más cercana (máximo 50 metros)
- **Score de accesibilidad**: Cálculo automático basado en cantidad y severidad de obstáculos (0-100)
- **Listo para visualización**: Geometrías GeoJSON y scores listos para usar en mapas

### Escala de Score
- **90-100**: Excelente accesibilidad (verde)
- **75-89**: Buena accesibilidad (verde claro)
- **50-74**: Accesibilidad moderada (amarillo)
- **25-49**: Baja accesibilidad (naranja)
- **0-24**: Muy inaccesible (rojo)

### Ejemplo de Respuesta
```json
{
  "city": "santiago",
  "total_obstacles": 1250,
  "sidewalks": [
    {
      "sidewalk_id": "sidewalk_0",
      "geometry": {
        "type": "LineString",
        "coordinates": [[-70.6483, -33.4569], [-70.6482, -33.4568]]
      },
      "position": {"lat": -33.4569, "lng": -70.6483},
      "accessibility_score": 85.5,
      "obstacle_count": 2,
      "severity_breakdown": {
        "bajo": 1,
        "medio": 1,
        "alto": 0,
        "critico": 0
      },
      "obstacles": [...]
    }
  ]
}
```

### Uso en Frontend
```javascript
// Ejemplo con Mapbox GL JS
sidewalks.forEach(sidewalk => {
  const color = getColorByScore(sidewalk.accessibility_score);
  map.addLayer({
    id: sidewalk.sidewalk_id,
    type: 'line',
    source: {
      type: 'geojson',
      data: {
        type: 'Feature',
        geometry: sidewalk.geometry
      }
    },
    paint: {
      'line-color': color,
      'line-width': 4
    }
  });
});
```
