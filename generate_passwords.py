#!/usr/bin/env python3
import bcrypt

usuarios = {
    'admin_gerente': 'Admin2024!',
    'maria_farm': 'Maria2024!',
    'jose_farm': 'Jose2024!',
    'ana_investigadora': 'Ana2024!',
    'luis_investigador': 'Luis2024!'
}

print("Generando hashes de contraseñas...")
print("=" * 80)

for username, password in usuarios.items():
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(f"Usuario: {username}")
    print(f"Contraseña: {password}")
    print(f"Hash: {hashed.decode()}")
    print("-" * 80)
