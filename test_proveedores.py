#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para verificar que se pueden leer proveedores correctamente
"""
from models.database import DatabaseManager
from models.mysql_models import MySQLModels

def test_proveedores():
    try:
        db_manager = DatabaseManager()
        mysql_models = MySQLModels(db_manager.mysql_conn)
        
        # Obtener proveedores
        proveedores = mysql_models.get_all_proveedores()
        
        print("✓ Proveedores encontrados:")
        print("-" * 80)
        for prov in proveedores:
            print(f"ID: {prov['id']}")
            print(f"Nombre: {prov['nombre']}")
            print(f"RFC: {prov.get('rfc', 'N/A')}")
            print(f"Activo: {'Sí' if prov['activo'] else 'No'}")
            print("-" * 80)
        
        print(f"\n✓ Total de proveedores activos: {len(proveedores)}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_proveedores()
