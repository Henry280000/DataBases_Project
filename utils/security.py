import bcrypt


def hash_password(password):
    """
    Hash de contraseña usando bcrypt
    
    Args:
        password (str): Contraseña en texto plano
    
    Returns:
        str: Hash de la contraseña
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, password_hash):
    """
    Verificar contraseña contra hash
    
    Args:
        password (str): Contraseña en texto plano
        password_hash (str): Hash almacenado
    
    Returns:
        bool: True si la contraseña es correcta
    """
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception as e:
        print(f"Error verificando contraseña: {e}")
        return False
