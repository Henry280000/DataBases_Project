#!/bin/bash

# ============================================
# PHARMAFLOW SOLUTIONS - Script de Instalación
# ============================================

echo "=================================================="
echo "   PharmaFlow Solutions - Instalación"
echo "=================================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}${NC} $1"
}

# Verificar Python
echo "1. Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python 3 no está instalado"
    echo "Instalar desde: https://www.python.org/downloads/"
    exit 1
fi

# Verificar MySQL
echo ""
echo "2. Verificando MySQL..."
if command -v mysql &> /dev/null; then
    MYSQL_VERSION=$(mysql --version)
    print_success "MySQL encontrado: $MYSQL_VERSION"
else
    print_error "MySQL no está instalado"
    echo "Instalar con: brew install mysql"
    exit 1
fi

# Verificar MongoDB
echo ""
echo "3. Verificando MongoDB..."
if command -v mongosh &> /dev/null; then
    print_success "MongoDB encontrado"
else
    print_warning "MongoDB no está instalado"
    echo "Instalar con: brew tap mongodb/brew && brew install mongodb-community"
fi

# Crear entorno virtual
echo ""
echo "4. Creando entorno virtual..."
if [ -d "venv" ]; then
    print_warning "Entorno virtual ya existe"
else
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
echo ""
echo "5. Activando entorno virtual..."
source venv/bin/activate
print_success "Entorno virtual activado"

# Instalar dependencias
echo ""
echo "6. Instalando dependencias Python..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
print_success "Dependencias instaladas"

# Configurar MySQL
echo ""
echo "7. Configuración de MySQL"
echo "=================================================="
read -p "¿Usuario root de MySQL? [root]: " MYSQL_USER
MYSQL_USER=${MYSQL_USER:-root}

read -sp "¿Contraseña root de MySQL?: " MYSQL_PASSWORD
echo ""

# Probar conexión MySQL
echo "Probando conexión a MySQL..."
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SELECT 1;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Conexión a MySQL exitosa"
else
    print_error "No se pudo conectar a MySQL"
    echo "Verificar usuario y contraseña"
    exit 1
fi

# Ejecutar scripts MySQL
echo ""
echo "8. Creando base de datos MySQL..."
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD < database/mysql_schema.sql
if [ $? -eq 0 ]; then
    print_success "Schema creado"
else
    print_error "Error creando schema"
    exit 1
fi

echo "Creando roles y privilegios..."
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD < database/mysql_roles_privileges.sql
print_success "Roles creados"

echo "Cargando datos iniciales..."
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD < database/mysql_data_seed.sql
print_success "Datos cargados"

# Configurar MongoDB
echo ""
echo "9. Configuración de MongoDB"
echo "=================================================="

# Verificar si MongoDB está corriendo
if pgrep -x "mongod" > /dev/null; then
    print_success "MongoDB está corriendo"
else
    print_warning "MongoDB no está corriendo"
    echo "Iniciando MongoDB..."
    brew services start mongodb-community
    sleep 3
fi

# Ejecutar scripts MongoDB (Python)
echo "Configurando MongoDB..."
python database/mongodb_setup.py
if [ $? -eq 0 ]; then
    print_success "MongoDB configurado"
else
    print_warning "Error configurando MongoDB"
    exit 1
fi

echo "Cargando datos MongoDB..."
python database/mongodb_seed.py
if [ $? -eq 0 ]; then
    print_success "Datos MongoDB cargados"
else
    print_warning "Error cargando datos MongoDB"
    exit 1
fi

# Crear directorios necesarios
echo ""
echo "10. Creando directorios..."
mkdir -p logs
mkdir -p uploads
print_success "Directorios creados"

# Resumen
echo ""
echo "=================================================="
echo "   INSTALACIÓN COMPLETADA"
echo "=================================================="
echo ""
echo "Para iniciar la aplicación:"
echo "  1. Activar entorno virtual: source venv/bin/activate"
echo "  2. Ejecutar: python app.py"
echo "  3. Abrir navegador: http://localhost:5000"
echo ""
echo "Usuarios de prueba:"
echo "  Gerente:       admin_gerente / PharmaFlow123!"
echo "  Farmacéutico:  maria_farm / PharmaFlow123!"
echo "  Investigador:  ana_investigadora / PharmaFlow123!"
echo ""
echo "=================================================="
