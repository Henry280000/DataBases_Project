import mysql.connector
from mysql.connector import pooling, Error
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import sys
from config.config import Config

#gestor generalizado de la sbases de datos
class DatabaseManager:    
    def __init__(self):
        self.mysql_pool = None
        self.mysql_conn = None
        self.mongo_client = None
        self.mongo_db = None
        
        # Inicializar conexiones
        self.connect_mysql()
        self.connect_mongodb()
    
    def connect_mysql(self):
        try:
            # Crear pool de conexiones
            self.mysql_pool = mysql.connector.pooling.MySQLConnectionPool(
                **Config.MYSQL_CONFIG
            )
            
            # Obtener una conexión de prueba
            self.mysql_conn = self.mysql_pool.get_connection()
            
            if self.mysql_conn.is_connected():
                cursor = self.mysql_conn.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                cursor.close()
                print(f"✓ Conectado a MySQL: {db_name}")
                return True
        
        except Error as e:
            print(f"✗ Error conectando a MySQL: {e}")
            sys.exit(1)
        
        return False
    
    def connect_mongodb(self):
        try:
            # Crear cliente MongoDB
            self.mongo_client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            
            # Verificar conexión
            self.mongo_client.admin.command('ping')
            
            # Obtener base de datos
            self.mongo_db = self.mongo_client[Config.MONGODB_CONFIG['database']]
            
            print(f"✓ Conectado a MongoDB: {Config.MONGODB_CONFIG['database']}")
            return True
        
        except (ConnectionFailure, OperationFailure) as e:
            print(f"✗ Error conectando a MongoDB: {e}")
            print("⚠ La aplicación continuará sin MongoDB (funcionalidad limitada)")
            self.mongo_db = None
            return False
    
    def get_mysql_connection(self):
        try:
            return self.mysql_pool.get_connection()
        except Error as e:
            print(f"Error obteniendo conexión MySQL: {e}")
            return None
    
    def close_all(self):
        try:
            if self.mysql_conn and self.mysql_conn.is_connected():
                self.mysql_conn.close()
                print("✓ Conexión MySQL cerrada")
        except:
            pass
        
        try:
            if self.mongo_client:
                self.mongo_client.close()
                print("✓ Conexión MongoDB cerrada")
        except:
            pass
    
    def test_connections(self):
        results = {
            'mysql': False,
            'mongodb': False
        }
        
        # Test MySQL
        try:
            if self.mysql_conn and self.mysql_conn.is_connected():
                cursor = self.mysql_conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                results['mysql'] = True
        except:
            pass
        
        # Test MongoDB
        try:
            if self.mongo_db:
                self.mongo_client.admin.command('ping')
                results['mongodb'] = True
        except:
            pass
        
        return results


# Función auxiliar para manejo de transacciones MySQL
class MySQLTransaction:
    
    def __init__(self, connection):
        self.connection = connection
        self.cursor = None
    
    def __enter__(self):
        self.cursor = self.connection.cursor(dictionary=True)
        self.connection.start_transaction()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Si hubo error, hacer rollback
            self.connection.rollback()
            print(f"Transacción revertida: {exc_val}")
            return False
        else:
            # Si todo salió bien, hacer commit
            self.connection.commit()
        
        if self.cursor:
            self.cursor.close()
        
        return True
