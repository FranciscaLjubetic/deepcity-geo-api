# 🚂 Guía de Despliegue en Railway

Railway es la mejor opción para desplegar APIs Python con dependencias pesadas.

## ✅ Ventajas de Railway sobre Vercel

- ✅ **Sin límite de 250 MB** en dependencias
- ✅ **Detecta Python automáticamente**
- ✅ **Deploy automático desde GitHub**
- ✅ **Más económico** ($5/mes con $5 gratis de crédito)
- ✅ **Mejor para APIs** con dependencias científicas (numpy, pandas, geopandas, etc.)
- ✅ **Variables de entorno fáciles**
- ✅ **Logs en tiempo real**

## 🚀 Pasos para desplegar en Railway

### 1. **Crear cuenta**
   - Ve a: https://railway.app
   - Click en **"Login"** o **"Start a New Project"**
   - Usa **"Login with GitHub"**

### 2. **Crear nuevo proyecto**
   - Click en **"New Project"**
   - Selecciona **"Deploy from GitHub repo"**
   - Busca: `FranciscaLjubetic/deepcity-geo-api`
   - Click en el repositorio

### 3. **Configuración automática**
   Railway detectará automáticamente:
   - ✅ Python project (por `requirements.txt`)
   - ✅ Puerto 8000 (de `main.py`)
   - ✅ Comando de inicio: `python main.py` o `uvicorn main:app`

### 4. **Variables de entorno (opcional)**
   En la sección **"Variables"**, agrega si necesitas:
   ```
   PORT=8000
   PYTHON_VERSION=3.11
   ```

### 5. **Deploy**
   - Railway comenzará a construir automáticamente
   - Espera 3-5 minutos (primera vez)
   - Te dará una URL como: `https://deepcity-geo-api-production.up.railway.app`

### 6. **Configurar dominio público**
   - Ve a **"Settings"** → **"Networking"**
   - Click en **"Generate Domain"**
   - Copia tu URL pública

## 📝 Archivos necesarios (ya los tienes)

- ✅ `requirements.txt` - Dependencias
- ✅ `runtime.txt` - Versión de Python (opcional)
- ✅ `main.py` - Aplicación FastAPI

## 🔧 Configuración opcional: Procfile

Si Railway no detecta el comando correcto, crea un `Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 🔄 Despliegues automáticos

Una vez configurado:
- ✅ Cada push a `main` → Deploy automático
- ✅ Pull requests → Preview deployments
- ✅ Logs en tiempo real

## 💰 Costos

- **Plan gratuito**: $5 de crédito gratis (suficiente para empezar)
- **Plan Developer**: $5/mes con $5 de crédito incluido
- **Sin cargos ocultos**: Solo pagas por lo que uses

## 🎯 Endpoints después del deploy

```
https://tu-proyecto.up.railway.app/
https://tu-proyecto.up.railway.app/docs
https://tu-proyecto.up.railway.app/health
https://tu-proyecto.up.railway.app/api/v1/cities/santiago/obstacles
```

## 🐛 Troubleshooting

### **Si el build falla:**
1. Ve a **"Deployments"** → Click en el deployment fallido
2. Revisa los logs
3. Verifica `requirements.txt`

### **Si el servicio no responde:**
1. Ve a **"Settings"** → **"Networking"**
2. Asegúrate de que el puerto sea `8000` o `$PORT`
3. Revisa que `main.py` tenga: `uvicorn.run(app, host="0.0.0.0", port=8000)`

### **Si necesitas más memoria:**
1. Ve a **"Settings"** → **"Resources"**
2. Aumenta la memoria asignada

## 📚 Recursos útiles

- Dashboard: https://railway.app/dashboard
- Documentación: https://docs.railway.app/
- Discord de soporte: https://discord.gg/railway

## ✅ Checklist de despliegue

- [ ] Cuenta de Railway creada
- [ ] Repositorio conectado
- [ ] Primera build exitosa
- [ ] URL pública generada
- [ ] Endpoints funcionando
- [ ] CORS configurado para tu frontend

---

## 🎉 ¡Listo!

Una vez desplegado, tu API estará disponible 24/7 sin las limitaciones de Vercel.

**¿Dudas?** Revisa los logs en Railway → son muy claros y te ayudarán a debuggear.
