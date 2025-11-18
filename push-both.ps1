# Script para pushear a ambos repositorios (origin y vercel)
# Uso: .\push-both.ps1 "mensaje de commit"

param(
    [string]$CommitMessage = ""
)

Write-Host "🚀 Pusheando a ambos repositorios..." -ForegroundColor Cyan
Write-Host ""

# Verificar si hay cambios para commitear
$hasChanges = git status --porcelain
if ($hasChanges) {
    Write-Host "📝 Hay cambios sin commitear" -ForegroundColor Yellow
    
    # Si no se proporciona mensaje, pedirlo
    if ([string]::IsNullOrEmpty($CommitMessage)) {
        $CommitMessage = Read-Host "💬 Ingresa el mensaje del commit"
    }
    
    Write-Host ""
    Write-Host "➕ Agregando archivos..." -ForegroundColor Gray
    git add .
    
    Write-Host "💾 Haciendo commit: $CommitMessage" -ForegroundColor Gray
    git commit -m $CommitMessage
    Write-Host ""
}

# Push a origin
Write-Host "📤 Pusheando a origin (deepcity-geo-api)..." -ForegroundColor Blue
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push a origin exitoso" -ForegroundColor Green
} else {
    Write-Host "❌ Error al pushear a origin" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Push a vercel
Write-Host "📤 Pusheando a vercel (deepcity-geo-api-v1)..." -ForegroundColor Blue
git push vercel main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push a vercel exitoso" -ForegroundColor Green
} else {
    Write-Host "❌ Error al pushear a vercel" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 ¡Código pusheado exitosamente a ambos repositorios!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Repositorios actualizados:" -ForegroundColor Cyan
Write-Host "   - origin: https://github.com/FranciscaLjubetic/deepcity-geo-api"
Write-Host "   - vercel: https://github.com/FranciscaLjubetic/deepcity-geo-api-v1"
Write-Host ""
Write-Host "🔄 Vercel desplegará automáticamente en unos minutos..." -ForegroundColor Yellow
Write-Host "   Dashboard: https://vercel.com/dashboard"
