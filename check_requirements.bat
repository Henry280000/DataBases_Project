@echo off
chcp 65001 >nul
echo ============================================
echo   Verificacion de Requisitos - Windows
echo ============================================
echo.

set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "NC=[0m"

echo Verificando requisitos previos...
echo.

REM Verificar Python
echo [1/6] Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%✗ Python NO instalado%NC%
    echo   Descarga: https://www.python.org/downloads/
    echo   IMPORTANTE: Marca "Add Python to PATH" durante instalacion
    set HAS_ERRORS=1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo %GREEN%✓ Python !PYTHON_VERSION! instalado%NC%
)
echo.

REM Verificar pip
echo [2/6] pip...
pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%✗ pip NO instalado%NC%
    set HAS_ERRORS=1
) else (
    echo %GREEN%✓ pip instalado%NC%
)
echo.

REM Verificar MySQL
echo [3/6] MySQL...
mysql --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%✗ MySQL NO instalado%NC%
    echo   Descarga: https://dev.mysql.com/downloads/installer/
    echo   Recomendado: MySQL Community Server 8.0
    set HAS_ERRORS=1
) else (
    for /f "tokens=3" %%i in ('mysql --version 2^>^&1') do set MYSQL_VERSION=%%i
    echo %GREEN%✓ MySQL !MYSQL_VERSION! instalado%NC%
    
    REM Verificar si MySQL esta corriendo
    sc query MySQL80 | find "RUNNING" >nul
    if %errorLevel% neq 0 (
        echo %YELLOW%⚠ MySQL no esta corriendo%NC%
        echo   Inicia el servicio MySQL80 desde Servicios de Windows
    ) else (
        echo %GREEN%✓ MySQL corriendo%NC%
    )
)
echo.

REM Verificar MongoDB
echo [4/6] MongoDB...
mongod --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%✗ MongoDB NO instalado%NC%
    echo   Descarga: https://www.mongodb.com/try/download/community
    set HAS_ERRORS=1
) else (
    for /f "tokens=3" %%i in ('mongod --version 2^>^&1 ^| findstr "version"') do set MONGO_VERSION=%%i
    echo %GREEN%✓ MongoDB instalado%NC%
    
    REM Verificar si MongoDB esta corriendo
    sc query MongoDB | find "RUNNING" >nul
    if %errorLevel% neq 0 (
        echo %YELLOW%⚠ MongoDB no esta corriendo%NC%
        echo   Esto es opcional - solo afecta ensayos clinicos
    ) else (
        echo %GREEN%✓ MongoDB corriendo%NC%
    )
)
echo.

REM Verificar Git
echo [5/6] Git...
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %YELLOW%⚠ Git NO instalado (opcional)%NC%
    echo   Descarga: https://git-scm.com/download/win
) else (
    for /f "tokens=3" %%i in ('git --version 2^>^&1') do set GIT_VERSION=%%i
    echo %GREEN%✓ Git !GIT_VERSION! instalado%NC%
)
echo.

REM Verificar permisos de administrador
echo [6/6] Permisos de Administrador...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo %YELLOW%⚠ NO ejecutando como Administrador%NC%
    echo   Para instalar, ejecuta install.bat como Administrador
) else (
    echo %GREEN%✓ Permisos de Administrador%NC%
)
echo.

echo ============================================
if defined HAS_ERRORS (
    echo %RED%FALTAN REQUISITOS%NC%
    echo.
    echo Instala los componentes faltantes antes de continuar.
) else (
    echo %GREEN%TODOS LOS REQUISITOS CUMPLIDOS%NC%
    echo.
    echo Puedes proceder con la instalacion:
    echo   1. Haz clic derecho en install.bat
    echo   2. Selecciona "Ejecutar como administrador"
)
echo ============================================
echo.
pause
