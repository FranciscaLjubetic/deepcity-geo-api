# 🚀 Scripts de Despliegue

Este directorio contiene scripts para facilitar el despliegue a ambos repositorios.

## 📜 Scripts disponibles

### **Windows (PowerShell): `push-both.ps1`**

#### Uso básico:
```powershell
# Con mensaje de commit
.\push-both.ps1 "feat: Agregar nueva funcionalidad"

# Sin mensaje (te lo pedirá)
.\push-both.ps1
```

#### Permisos (primera vez):
Si PowerShell bloquea la ejecución, ejecuta esto primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Linux/Mac (Bash): `push-both.sh`**

#### Uso básico:
```bash
# Dar permisos de ejecución (solo primera vez)
chmod +x push-both.sh

# Con mensaje de commit
./push-both.sh "feat: Agregar nueva funcionalidad"

# Sin mensaje (te lo pedirá)
./push-both.sh
```

## 🎯 ¿Qué hacen estos scripts?

1. ✅ Detectan si hay cambios sin commitear
2. ✅ Te piden un mensaje de commit (si no lo proporcionas)
3. ✅ Hacen `git add .` y `git commit`
4. ✅ Pushean a **origin** (deepcity-geo-api)
5. ✅ Pushean a **vercel** (deepcity-geo-api-v1)
6. ✅ Muestran confirmación de éxito

## 📦 Repositorios configurados

- **origin**: https://github.com/FranciscaLjubetic/deepcity-geo-api
  - Repositorio principal
  
- **vercel**: https://github.com/FranciscaLjubetic/deepcity-geo-api-v1
  - Repositorio conectado a Vercel para despliegue automático

## 🔄 Workflow recomendado

1. Haz cambios en tu código
2. Ejecuta el script:
   ```powershell
   .\push-both.ps1 "Descripción de los cambios"
   ```
3. Espera 2-3 minutos
4. Verifica el despliegue en: https://vercel.com/dashboard

## 💡 Tips

- Los scripts detectan automáticamente si hay cambios
- Si no hay cambios, solo harán push de los commits existentes
- Puedes seguir usando `git` manualmente si lo prefieres
- Los cambios en `vercel` disparan despliegue automático en Vercel

## ⚠️ Nota importante

Siempre asegúrate de probar tu código localmente antes de pushear:
```bash
# Probar localmente
python main.py

# Acceder a
http://localhost:8000/docs
```
