#!/bin/bash

echo "============================================"
echo "  PharmaFlow Solutions - Actualización"
echo "============================================"
echo ""

echo "Descargando últimos cambios desde GitHub..."
git pull

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: No se pudo descargar los cambios"
    echo "Verifica tu conexión a internet y que tengas Git instalado"
    exit 1
fi

echo ""
echo "Actualización completada con éxito"
echo ""
echo "Si hubo cambios en:"
echo "  - Base de datos: Ejecuta ./install.sh"
echo "  - Solo código: Ejecuta ./start.sh normalmente"
echo ""
echo "============================================"
