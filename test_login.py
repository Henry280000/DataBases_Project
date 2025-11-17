#!/usr/bin/env python3
# Script para probar el login de usuarios

import sys
sys.path.insert(0, '/Users/enrique/Documents/Programacion/proyecto 2 bases de datos')

from models.database import DatabaseManager
from models.mysql_models import MySQLModels
from utils.security import verify_password

# Inicializar
db_manager = DatabaseManager()
mysql_models = MySQLModels(db_manager.mysql_conn)

# Usuarios a probar
usuarios_prueba = [
    ('admin_gerente', 'Admin2024!'),
    ('maria_farm', 'Maria2024!'),
    ('jose_farm', 'Jose2024!'),
    ('ana_investigadora', 'Ana2024!'),
    ('luis_investigador', 'Luis2024!')
]

print("=" * 80)
print("PROBANDO LOGIN DE USUARIOS")
print("=" * 80)

for username, password in usuarios_prueba:
    print(f"\nProbando: {username} / {password}")
    
    # Buscar usuario
    user = mysql_models.get_user_by_username(username)
    
    if not user:
        print(f"  ❌ Usuario '{username}' NO encontrado en la base de datos")
        continue
    
    print(f"  ✓ Usuario encontrado: {user['nombre_completo']}")
    print(f"  ✓ Rol: {user['rol']}")
    print(f"  ✓ Activo: {user['activo']}")
    
    # Verificar contraseña
    if verify_password(password, user['password_hash']):
        print(f"  ✅ Contraseña CORRECTA - Login exitoso!")
    else:
        print(f"  ❌ Contraseña INCORRECTA - Login fallido")

print("\n" + "=" * 80)
