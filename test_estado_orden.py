#!/usr/bin/env python3
"""
Script para probar el cambio de estado de orden
"""
import sys
sys.path.insert(0, '/Users/enrique/Documents/Programacion/proyecto 2 bases de datos')

from models.database import DatabaseManager
from models.mysql_models import MySQLModels

db_manager = DatabaseManager()
mysql_conn = db_manager.get_mysql_connection()
mysql_models = MySQLModels(mysql_conn)

# Obtener estadísticas ANTES del cambio
print("=== ESTADÍSTICAS ANTES ===")
stats_antes = mysql_models.get_estadisticas_inventario()
print(f"Total medicamentos: {stats_antes['total_medicamentos']}")
print(f"Total lotes: {stats_antes['total_lotes']}")
print(f"Unidades totales: {stats_antes['unidades_total']}")
print(f"Valor total: ${stats_antes['valor_total']}")
print(f"Lotes por caducar: {stats_antes['lotes_proximos_caducar']}")

# Cambiar orden TEST-DASH (id=8) a Recibida
print("\n=== PROCESANDO ORDEN ===")
print("Cambiando orden 8 (TEST-DASH) a estado 'Recibida'...")
result = mysql_models.update_orden_estado(8, 'Recibida')
print(f"Resultado: {result}")

# Obtener estadísticas DESPUÉS del cambio
print("\n=== ESTADÍSTICAS DESPUÉS ===")
stats_despues = mysql_models.get_estadisticas_inventario()
print(f"Total medicamentos: {stats_despues['total_medicamentos']}")
print(f"Total lotes: {stats_despues['total_lotes']}")
print(f"Unidades totales: {stats_despues['unidades_total']}")
print(f"Valor total: ${stats_despues['valor_total']}")
print(f"Lotes por caducar: {stats_despues['lotes_proximos_caducar']}")

# Verificar diferencias
print("\n=== CAMBIOS ===")
print(f"Incremento en lotes: {stats_despues['total_lotes'] - stats_antes['total_lotes']}")
print(f"Incremento en unidades: {stats_despues['unidades_total'] - stats_antes['unidades_total']}")
print(f"Incremento en valor: ${float(stats_despues['valor_total']) - float(stats_antes['valor_total'])}")

# Verificar lote creado
print("\n=== LOTE CREADO ===")
lotes = mysql_models._execute_query(
    "SELECT codigo_lote, id_medicamento, cantidad_inicial, cantidad_actual, estado FROM lotes WHERE codigo_lote LIKE 'LOTE-2025%' ORDER BY codigo_lote DESC LIMIT 1"
)
if lotes:
    print(f"Último lote: {lotes[0]['codigo_lote']} - Med ID: {lotes[0]['id_medicamento']} - Cantidad: {lotes[0]['cantidad_actual']} - Estado: {lotes[0]['estado']}")
