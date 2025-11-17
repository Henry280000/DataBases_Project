#!/usr/bin/env python3
"""
Script para probar que se obtienen medicamentos correctamente
"""
import sys
sys.path.insert(0, '/Users/enrique/Documents/Programacion/proyecto 2 bases de datos')

from models.database import DatabaseManager
from models.mysql_models import MySQLModels

def test_medicamentos():
    db_manager = DatabaseManager()
    mysql = MySQLModels(db_manager.mysql_conn)
    
    print("=" * 50)
    print("PRUEBA: Obtener medicamentos")
    print("=" * 50)
    
    medicamentos = mysql.get_all_medicamentos()
    
    print(f"\n✓ Total medicamentos obtenidos: {len(medicamentos)}")
    
    if medicamentos:
        print("\n--- Primeros 5 medicamentos ---")
        for i, med in enumerate(medicamentos[:5], 1):
            print(f"\n{i}. ID: {med.get('id')}")
            print(f"   Nombre: {med.get('nombre')}")
            print(f"   Categoría: {med.get('categoria_nombre')}")
            print(f"   Principio Activo: {med.get('principio_activo')}")
            print(f"   Stock: {med.get('stock_total')}")
    else:
        print("\n⚠ No se encontraron medicamentos")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_medicamentos()
