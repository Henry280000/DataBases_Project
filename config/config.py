import os
from datetime import timedelta

class Config:
    # Configuración general
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pharmaflow-secret-key-2024-desarrollo'
    PORT = int(os.environ.get('PORT', 5001))
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de MySQL
    MYSQL_CONFIG = {
        'host': os.environ.get('MYSQL_HOST', 'localhost'),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
        'user': os.environ.get('MYSQL_USER', 'pharmaflow_app'),
        'password': os.environ.get('MYSQL_PASSWORD', 'AppPharma2024!'),
        'database': os.environ.get('MYSQL_DATABASE', 'pharmaflow_relational'),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci',
        'autocommit': False,
        'pool_name': 'pharmaflow_pool',
        'pool_size': 5,
        'pool_reset_session': True
    }
    
    # Configuración de MongoDB 
    MONGODB_CONFIG = {
        'host': os.environ.get('MONGODB_HOST', 'localhost'),
        'port': int(os.environ.get('MONGODB_PORT', 27017)),
        'database': os.environ.get('MONGODB_DATABASE', 'pharmaflow_nosql')
    }
    
    # URI de conexión MongoDB simplificada (sin autenticación)
    MONGODB_URI = f"mongodb://{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}"


class DevelopmentConfig(Config):
    # Configuración de desarrollo
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    # Configuración de producción
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    # Configuración de testing
    TESTING = True
    DEBUG = True
    
    # Base de datos de pruebas
    MYSQL_CONFIG = Config.MYSQL_CONFIG.copy()
    MYSQL_CONFIG['database'] = 'pharmaflow_test'
    
    MONGODB_CONFIG = Config.MONGODB_CONFIG.copy()
    MONGODB_CONFIG['database'] = 'pharmaflow_test'


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
