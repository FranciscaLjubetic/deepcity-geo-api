#!/bin/bash

# Script para pushear a ambos repositorios (origin y vercel)
# Uso: ./push-both.sh [mensaje de commit opcional]

echo "🚀 Pusheando a ambos repositorios..."
echo ""

# Verificar si hay cambios para commitear
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Hay cambios sin commitear"
    
    # Si se proporciona un mensaje de commit, usarlo
    if [ -n "$1" ]; then
        COMMIT_MSG="$1"
    else
        echo "💬 Ingresa el mensaje del commit:"
        read COMMIT_MSG
    fi
    
    echo ""
    echo "➕ Agregando archivos..."
    git add .
    
    echo "💾 Haciendo commit: $COMMIT_MSG"
    git commit -m "$COMMIT_MSG"
    echo ""
fi

# Push a origin
echo "📤 Pusheando a origin (deepcity-geo-api)..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Push a origin exitoso"
else
    echo "❌ Error al pushear a origin"
    exit 1
fi

echo ""

# Push a vercel
echo "📤 Pusheando a vercel (deepcity-geo-api-v1)..."
git push vercel main

if [ $? -eq 0 ]; then
    echo "✅ Push a vercel exitoso"
else
    echo "❌ Error al pushear a vercel"
    exit 1
fi

echo ""
echo "🎉 ¡Código pusheado exitosamente a ambos repositorios!"
echo ""
echo "📍 Repositorios actualizados:"
echo "   - origin: https://github.com/FranciscaLjubetic/deepcity-geo-api"
echo "   - vercel: https://github.com/FranciscaLjubetic/deepcity-geo-api-v1"
echo ""
echo "🔄 Vercel desplegará automáticamente en unos minutos..."
echo "   Dashboard: https://vercel.com/dashboard"
