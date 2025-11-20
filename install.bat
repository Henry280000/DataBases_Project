@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================
echo   PharmaFlow Solutions - Instalador Windows
echo ============================================
echo.

REM Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Este script debe ejecutarse como Administrador
    echo.
    echo Haz clic derecho en install.bat y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

REM Colores para mensajes
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "NC=[0m"

echo [Paso 1/10] Verificando requisitos previos...
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%ERROR: Python no esta instalado%NC%
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)
echo %GREEN%✓ Python instalado%NC%

REM Verificar MySQL
mysql --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%ERROR: MySQL no esta instalado%NC%
    echo.
    echo Descarga MySQL desde: https://dev.mysql.com/downloads/installer/
    pause
    exit /b 1
)
echo %GREEN%✓ MySQL instalado%NC%

REM Verificar si MySQL esta corriendo
sc query MySQL80 | find "RUNNING" >nul
if %errorLevel% neq 0 (
    echo %YELLOW%MySQL no esta corriendo. Iniciando...%NC%
    net start MySQL80 >nul 2>&1
    if %errorLevel% neq 0 (
        echo %RED%ERROR: No se pudo iniciar MySQL%NC%
        echo Inicia MySQL manualmente desde Servicios de Windows
        pause
        exit /b 1
    )
)
echo %GREEN%✓ MySQL corriendo%NC%

REM Verificar MongoDB
mongod --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%ERROR: MongoDB no esta instalado%NC%
    echo.
    echo Descarga MongoDB desde: https://www.mongodb.com/try/download/community
    pause
    exit /b 1
)
echo %GREEN%✓ MongoDB instalado%NC%

REM Verificar si MongoDB esta corriendo
sc query MongoDB | find "RUNNING" >nul
if %errorLevel% neq 0 (
    echo %YELLOW%MongoDB no esta corriendo. Iniciando...%NC%
    net start MongoDB >nul 2>&1
    if %errorLevel% neq 0 (
        echo %YELLOW%Advertencia: MongoDB podria no estar configurado como servicio%NC%
        echo Puedes iniciarlo manualmente despues
    )
)
echo %GREEN%✓ MongoDB corriendo%NC%

echo.
echo [Paso 2/10] Configurando credenciales MySQL...
echo.
set /p MYSQL_ROOT_PASSWORD="Ingresa la contraseña de root de MySQL: "
set /p MYSQL_USER="Usuario de la aplicacion (default: pharmaflow_app): " || set MYSQL_USER=pharmaflow_app
set /p MYSQL_PASSWORD="Contraseña de la aplicacion (default: AppPharma2024!): " || set MYSQL_PASSWORD=AppPharma2024!

echo.
echo [Paso 3/10] Creando entorno virtual...
if exist venv (
    echo Eliminando entorno virtual antiguo...
    rmdir /s /q venv
)
python -m venv venv
if %errorLevel% neq 0 (
    echo %RED%ERROR: No se pudo crear el entorno virtual%NC%
    pause
    exit /b 1
)
echo %GREEN%✓ Entorno virtual creado%NC%

echo.
echo [Paso 4/10] Activando entorno virtual e instalando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo %RED%ERROR: No se pudieron instalar las dependencias%NC%
    pause
    exit /b 1
)
echo %GREEN%✓ Dependencias instaladas%NC%

echo.
echo [Paso 5/10] Configurando base de datos MySQL...

REM Crear archivo temporal de configuracion MySQL
set TEMP_MYSQL_CONFIG=%TEMP%\mysql_config_%RANDOM%.cnf
(
echo [client]
echo user=root
echo password=%MYSQL_ROOT_PASSWORD%
) > "%TEMP_MYSQL_CONFIG%"

REM Ejecutar scripts SQL
echo Ejecutando schema...
mysql --defaults-extra-file="%TEMP_MYSQL_CONFIG%" < database\mysql_schema.sql 2>nul
if %errorLevel% neq 0 (
    echo %RED%ERROR: Fallo al crear el schema%NC%
    del "%TEMP_MYSQL_CONFIG%"
    pause
    exit /b 1
)

echo Configurando roles y privilegios...
mysql --defaults-extra-file="%TEMP_MYSQL_CONFIG%" < database\mysql_roles_privileges.sql 2>nul

echo Insertando datos iniciales...
mysql --defaults-extra-file="%TEMP_MYSQL_CONFIG%" < database\mysql_data_seed.sql 2>nul

REM Eliminar archivo temporal
del "%TEMP_MYSQL_CONFIG%"

echo %GREEN%✓ Base de datos MySQL configurada%NC%

echo.
echo [Paso 6/10] Configurando MongoDB...

REM Verificar conexion a MongoDB
mongosh --quiet --eval "db.version()" >nul 2>&1
if %errorLevel% neq 0 (
    echo %YELLOW%Advertencia: No se pudo conectar a MongoDB%NC%
    echo MongoDB podria no estar corriendo. Intentando continuar...
) else (
    echo Ejecutando setup de MongoDB...
    python database\mongodb_setup.py
    if %errorLevel% neq 0 (
        echo %YELLOW%Advertencia: Problema al configurar MongoDB%NC%
    ) else (
        echo %GREEN%✓ MongoDB configurado%NC%
    )
    
    echo Insertando datos de prueba en MongoDB...
    python database\mongodb_seed.py
    if %errorLevel% neq 0 (
        echo %YELLOW%Advertencia: Problema al insertar datos en MongoDB%NC%
    ) else (
        echo %GREEN%✓ Datos insertados en MongoDB%NC%
    )
)

echo.
echo [Paso 7/10] Creando archivo de configuracion .env...
(
echo # Configuracion de la aplicacion PharmaFlow
echo.
echo # MySQL
echo MYSQL_HOST=localhost
echo MYSQL_PORT=3306
echo MYSQL_USER=%MYSQL_USER%
echo MYSQL_PASSWORD=%MYSQL_PASSWORD%
echo MYSQL_DATABASE=pharmaflow_relational
echo.
echo # MongoDB
echo MONGODB_HOST=localhost
echo MONGODB_PORT=27017
echo MONGODB_DATABASE=pharmaflow_nosql
echo.
echo # Flask
echo SECRET_KEY=pharmaflow-secret-key-2024-desarrollo
echo FLASK_ENV=development
echo PORT=5001
) > .env
echo %GREEN%✓ Archivo .env creado%NC%

echo.
echo [Paso 8/10] Generando contraseñas hasheadas para usuarios...
python generate_passwords.py >nul 2>&1
if %errorLevel% equ 0 (
    echo %GREEN%✓ Contraseñas generadas%NC%
) else (
    echo %YELLOW%Advertencia: No se pudieron generar contraseñas%NC%
)

echo.
echo [Paso 9/10] Verificando instalacion...

REM Verificar tablas MySQL
mysql --defaults-extra-file="%TEMP%\mysql_verify_%RANDOM%.cnf" -u %MYSQL_USER% -p%MYSQL_PASSWORD% pharmaflow_relational -e "SHOW TABLES;" >nul 2>&1
if %errorLevel% neq 0 (
    echo %YELLOW%Advertencia: Problema al verificar MySQL%NC%
) else (
    echo %GREEN%✓ MySQL funcionando correctamente%NC%
)

echo.
echo [Paso 10/10] Creando script de inicio...
(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python app.py
echo pause
) > start.bat
echo %GREEN%✓ Script de inicio creado%NC%

echo.
echo ============================================
echo   INSTALACION COMPLETADA CON EXITO
echo ============================================
echo.
echo Para iniciar la aplicacion:
echo   1. Ejecuta: start.bat
echo   2. Abre tu navegador en: http://localhost:5001
echo.
echo Credenciales por defecto:
echo   Admin:         admin / admin123
echo   Medico:        medico / medico123
echo   Farmaceutico:  farmaceutico / farmaceutico123
echo.
echo ============================================
pause
