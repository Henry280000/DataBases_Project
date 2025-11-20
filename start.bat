@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   PharmaFlow Solutions - Iniciando...
echo ============================================
echo.

REM Verificar si existe el entorno virtual
if not exist venv (
    echo ERROR: No se encontro el entorno virtual.
    echo Por favor, ejecuta install.bat primero.
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar MySQL
sc query MySQL80 | find "RUNNING" >nul
if %errorLevel% neq 0 (
    echo MySQL no esta corriendo. Iniciando...
    net start MySQL80 >nul 2>&1
    if %errorLevel% neq 0 (
        echo ADVERTENCIA: No se pudo iniciar MySQL automaticamente
        echo Por favor, inicia MySQL manualmente
        pause
    )
)

REM Verificar MongoDB
sc query MongoDB | find "RUNNING" >nul
if %errorLevel% neq 0 (
    echo MongoDB no esta corriendo. Iniciando...
    net start MongoDB >nul 2>&1
    if %errorLevel% neq 0 (
        echo ADVERTENCIA: MongoDB podria no estar corriendo
        echo Si tienes problemas con ensayos clinicos, inicia MongoDB manualmente
    )
)

echo.
echo Iniciando aplicacion en http://localhost:5001
echo Presiona Ctrl+C para detener
echo.

REM Iniciar la aplicacion
python app.py

pause
