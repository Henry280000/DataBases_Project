#!/bin/bash
# Activar entorno virtual
source venv/bin/activate

# Verificar que las bases de datos estén corriendo
echo "Verificando servicios..."

# MySQL
if ! pgrep -x "mysqld" > /dev/null; then
    echo " MySQL no está corriendo"
    echo "Iniciarlo con: brew services start mysql"
    exit 1
fi

# MongoDB (opcional)
if ! pgrep -x "mongod" > /dev/null; then
    echo " MongoDB no está corriendo (funcionalidad limitada)"
    echo "Iniciarlo con: brew services start mongodb-community"
fi

# Iniciar aplicación
echo ""
echo "=================================================="
echo "   Iniciando PharmaFlow Solutions..."
echo "=================================================="
echo ""

python app.py
