@echo off
chcp 65001 >nul
echo ============================================
echo   PharmaFlow Solutions - Actualizacion
echo ============================================
echo.

echo Descargando ultimos cambios desde GitHub...
git pull

if %errorLevel% neq 0 (
    echo.
    echo ERROR: No se pudo descargar los cambios
    echo Verifica tu conexion a internet y que tengas Git instalado
    pause
    exit /b 1
)

echo.
echo Actualizacion completada con exito
echo.
echo Si hubo cambios en:
echo   - Base de datos: Ejecuta install.bat como administrador
echo   - Solo codigo: Ejecuta start.bat normalmente
echo.
echo ============================================
pause
