#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para verificar que UTF-8 funciona correctamente
"""
import mysql.connector
from config.config import Config

def test_utf8():
    try:
        # Conectar a MySQL
        conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Configurar UTF-8
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        
        # Consultar categorías con acentos
        cursor.execute("SELECT nombre, descripcion FROM categorias LIMIT 5")
        
        print("✓ Prueba de UTF-8:")
        print("-" * 80)
        for nombre, descripcion in cursor.fetchall():
            print(f"Nombre: {nombre}")
            print(f"Descripción: {descripcion}")
            print("-" * 80)
        
        cursor.close()
        conn.close()
        print("\n✓ UTF-8 funciona correctamente!")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_utf8()
