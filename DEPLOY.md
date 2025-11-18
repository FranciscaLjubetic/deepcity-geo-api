# 🚀 Guía de Despliegue en Vercel

## Pasos para desplegar tu API en Vercel

### 1. **Crear cuenta en Vercel (si no tienes)**
- Ve a: https://vercel.com/signup
- Regístrate con tu cuenta de GitHub

### 2. **Conectar tu repositorio de GitHub a Vercel**

#### Opción A: Desde el sitio web de Vercel
1. Ve a: https://vercel.com/new
2. Click en **"Import Git Repository"**
3. Selecciona tu cuenta de GitHub: **FranciscaLjubetic**
4. Busca y selecciona el repositorio: **deepcity-geo-api**
5. Click en **"Import"**

#### Opción B: Desde la terminal (Vercel CLI)
```bash
# Instalar Vercel CLI globalmente
npm install -g vercel

# Login a Vercel
vercel login

# Desplegar
vercel --prod
```

### 3. **Configuración del proyecto en Vercel**

Cuando Vercel te pida configuración, usa estos valores:

- **Framework Preset:** `Other`
- **Build Command:** (dejar vacío)
- **Output Directory:** (dejar vacío)
- **Install Command:** `pip install -r requirements.txt`

### 4. **Variables de entorno (opcional)**

Si necesitas agregar variables de entorno:
1. En el dashboard de Vercel, ve a tu proyecto
2. Click en **"Settings"** → **"Environment Variables"**
3. Agrega las variables que necesites

### 5. **Verificar el despliegue**

Una vez desplegado, Vercel te dará una URL como:
```
https://deepcity-geo-api.vercel.app
```

Prueba los endpoints:
- `https://deepcity-geo-api.vercel.app/`
- `https://deepcity-geo-api.vercel.app/docs`
- `https://deepcity-geo-api.vercel.app/health`
- `https://deepcity-geo-api.vercel.app/api/v1/cities/santiago/obstacles`

## 🔄 **Despliegues automáticos**

Una vez conectado, Vercel desplegará automáticamente:
- ✅ Cada push a la rama `main` → Despliegue a producción
- ✅ Cada pull request → Preview deployment

## ⚙️ **Configuración actual del proyecto**

Tu proyecto ya tiene:
- ✅ `vercel.json` configurado
- ✅ `requirements.txt` con todas las dependencias
- ✅ Python 3.11 especificado
- ✅ CORS habilitado para permitir requests desde cualquier origen

## 📝 **Notas importantes**

1. **Primera vez puede tardar:** El primer despliegue puede tomar 2-5 minutos
2. **Cold starts:** Las funciones serverless pueden tener "cold starts" (1-3 segundos la primera vez)
3. **Límites de Vercel (Free tier):**
   - Límite de tiempo de ejecución: 10 segundos por request
   - Límite de memoria: 1024 MB
   - Límite de tamaño: 250 MB (incluye dependencias)

## 🐛 **Si hay errores**

1. **Ver logs:** En Vercel Dashboard → tu proyecto → "Deployments" → click en el deployment → "View Function Logs"
2. **Revisar build:** Verifica que todas las dependencias estén en `requirements.txt`
3. **Probar localmente:** `vercel dev` simula el entorno de Vercel localmente

## 🔗 **Enlaces útiles**

- Dashboard de Vercel: https://vercel.com/dashboard
- Documentación de Vercel para Python: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- Tu repositorio: https://github.com/FranciscaLjubetic/deepcity-geo-api

## ✅ **Checklist antes de desplegar**

- [x] Código pusheado a GitHub
- [x] `vercel.json` configurado
- [x] `requirements.txt` actualizado
- [x] CORS configurado
- [ ] Cuenta de Vercel creada
- [ ] Repositorio conectado a Vercel
- [ ] Primer despliegue exitoso

---

¡Listo! Una vez que completes estos pasos, tu API estará disponible públicamente en Vercel. 🎉
