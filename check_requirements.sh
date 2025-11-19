#!/bin/bash

# ============================================
# PHARMAFLOW - Verificación de Requisitos
# ============================================

echo "=================================================="
echo "   Verificación de Requisitos Previos"
echo "=================================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ERRORS=$((ERRORS + 1))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

# 1. Python
echo "1. Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
        print_success "Python $PYTHON_VERSION (OK)"
    else
        print_warning "Python $PYTHON_VERSION (se recomienda 3.9+)"
    fi
else
    print_error "Python 3 no está instalado"
    echo "   Instalar: https://www.python.org/downloads/"
fi

# 2. pip
echo ""
echo "2. Verificando pip..."
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    print_success "pip está disponible"
else
    print_error "pip no está instalado"
    echo "   Instalar: python3 -m ensurepip --upgrade"
fi

# 3. MySQL
echo ""
echo "3. Verificando MySQL..."
if command -v mysql &> /dev/null; then
    MYSQL_VERSION=$(mysql --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    print_success "MySQL $MYSQL_VERSION instalado"
    
    # Verificar si está corriendo
    if pgrep -x "mysqld" > /dev/null; then
        print_success "MySQL está corriendo"
    else
        print_warning "MySQL no está corriendo"
        echo "   Iniciar: brew services start mysql (macOS)"
        echo "   O: sudo systemctl start mysql (Linux)"
    fi
else
    print_error "MySQL no está instalado"
    echo "   Instalar macOS: brew install mysql"
    echo "   Instalar Linux: sudo apt-get install mysql-server"
fi

# 4. MongoDB
echo ""
echo "4. Verificando MongoDB..."
if command -v mongosh &> /dev/null; then
    print_success "mongosh está instalado"
    
    # Verificar si está corriendo
    if pgrep -x "mongod" > /dev/null; then
        print_success "MongoDB está corriendo"
        
        # Probar conexión
        if mongosh --quiet --eval "db.version()" > /dev/null 2>&1; then
            MONGO_VERSION=$(mongosh --quiet --eval "db.version()")
            print_success "Conexión a MongoDB OK (versión: $MONGO_VERSION)"
        else
            print_warning "No se puede conectar a MongoDB"
        fi
    else
        print_warning "MongoDB no está corriendo"
        echo "   Iniciar: brew services start mongodb-community (macOS)"
        echo "   O: sudo systemctl start mongod (Linux)"
    fi
else
    print_error "MongoDB/mongosh no está instalado"
    echo "   Instalar macOS: brew tap mongodb/brew && brew install mongodb-community"
    echo "   Instalar Linux: https://www.mongodb.com/docs/manual/administration/install-on-linux/"
fi

# 5. Git
echo ""
echo "5. Verificando Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    print_success "Git $GIT_VERSION instalado"
else
    print_warning "Git no está instalado"
    echo "   Instalar: https://git-scm.com/downloads"
fi

# 6. Conectividad MySQL
echo ""
echo "6. Probando conexión MySQL..."
read -p "¿Probar conexión a MySQL? (s/n) [s]: " TEST_MYSQL
TEST_MYSQL=${TEST_MYSQL:-s}

if [ "$TEST_MYSQL" = "s" ]; then
    read -p "Usuario MySQL [root]: " MYSQL_USER
    MYSQL_USER=${MYSQL_USER:-root}
    read -sp "Contraseña MySQL: " MYSQL_PASS
    echo ""
    
    if mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "SELECT 1;" > /dev/null 2>&1; then
        print_success "Conexión a MySQL exitosa"
    else
        print_error "No se pudo conectar a MySQL"
        echo "   Verifica usuario y contraseña"
    fi
fi

# Resumen
echo ""
echo "=================================================="
echo "   RESUMEN"
echo "=================================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ Todos los requisitos están listos${NC}"
    echo ""
    echo "Puedes continuar con la instalación:"
    echo "  ./install.sh"
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Hay $WARNINGS advertencia(s)${NC}"
    echo ""
    echo "Puedes intentar la instalación, pero revisa las advertencias."
    echo "  ./install.sh"
else
    echo -e "${RED}✗ Hay $ERRORS error(es) que debes resolver${NC}"
    echo ""
    echo "Resuelve los errores antes de continuar."
    echo "Consulta: INSTALACION.md"
    exit 1
fi

echo ""
