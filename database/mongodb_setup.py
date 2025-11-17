import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import CollectionInvalid, OperationFailure
from config.config import Config

def setup_mongodb():
    # Configurar MongoDB: crear colecciones, validaciones e índices
    
    print("=" * 60)
    print("PHARMAFLOW SOLUTIONS - Configuración MongoDB")
    print("=" * 60)
    print()
    
    try:
        # Conectar a MongoDB
        print("1. Conectando a MongoDB...")
        client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print(f"   ✓ Conectado a: {Config.MONGODB_URI}")
        
        # Seleccionar base de datos
        db = client[Config.MONGODB_CONFIG['database']]
        print(f"   Base de datos: {Config.MONGODB_CONFIG['database']}")
        print()
        
        # coleccion: clinical_trials

        print("2. Creando colección: clinical_trials")
        
        clinical_trials_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["trial_id", "titulo", "medicamento_id", "fase", "fecha_inicio", "estado"],
                "properties": {
                    "trial_id": {
                        "bsonType": "string",
                        "description": "Identificador único del ensayo clínico"
                    },
                    "titulo": {
                        "bsonType": "string",
                        "description": "Título del ensayo clínico"
                    },
                    "medicamento_id": {
                        "bsonType": "int",
                        "description": "ID del medicamento (referencia a MySQL)"
                    },
                    "medicamento_nombre": {
                        "bsonType": "string",
                        "description": "Nombre del medicamento"
                    },
                    "principio_activo": {
                        "bsonType": "string",
                        "description": "Principio activo del medicamento"
                    },
                    "fase": {
                        "enum": ["Fase I", "Fase II", "Fase III", "Fase IV"],
                        "description": "Fase del ensayo clínico"
                    },
                    "fecha_inicio": {
                        "bsonType": "date",
                        "description": "Fecha de inicio del ensayo"
                    },
                    "fecha_finalizacion": {
                        "bsonType": ["date", "null"],
                        "description": "Fecha de finalización (null si está en curso)"
                    },
                    "estado": {
                        "enum": ["Planificado", "En Curso", "Completado", "Suspendido", "Cancelado"],
                        "description": "Estado actual del ensayo"
                    },
                    "objetivo_principal": {
                        "bsonType": "string",
                        "description": "Objetivo principal del estudio"
                    }
                }
            }
        }
        
        try:
            db.create_collection("clinical_trials", validator=clinical_trials_validator)
            print("   Colección creada con validación")
        except CollectionInvalid:
            print("   Colección ya existe, actualizando validación...")
            db.command({
                "collMod": "clinical_trials",
                "validator": clinical_trials_validator
            })
        
        # Índices para clinical_trials
        print("   Creando índices...")
        db.clinical_trials.create_index([("trial_id", ASCENDING)], unique=True)
        db.clinical_trials.create_index([("medicamento_id", ASCENDING)])
        db.clinical_trials.create_index([("fase", ASCENDING)])
        db.clinical_trials.create_index([("estado", ASCENDING)])
        db.clinical_trials.create_index([("fecha_inicio", DESCENDING)])
        db.clinical_trials.create_index([
            ("titulo", TEXT),
            ("objetivo_principal", TEXT),
            ("principio_activo", TEXT)
        ], name="search_index")
        print("   Índices creados")
        print()
        
        # coleccion: research_reports
        print("3. Creando colección: research_reports")
        
        research_reports_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["report_id", "trial_id", "fecha_reporte", "investigador", "tipo_reporte"],
                "properties": {
                    "report_id": {
                        "bsonType": "string",
                        "description": "Identificador único del reporte"
                    },
                    "trial_id": {
                        "bsonType": "string",
                        "description": "ID del ensayo clínico asociado"
                    },
                    "fecha_reporte": {
                        "bsonType": "date",
                        "description": "Fecha de creación del reporte"
                    },
                    "investigador": {
                        "bsonType": "object",
                        "required": ["nombre", "id_usuario"],
                        "description": "Información del investigador"
                    },
                    "tipo_reporte": {
                        "enum": ["Seguimiento", "Intermedio", "Final", "Evento Adverso"],
                        "description": "Tipo de reporte"
                    }
                }
            }
        }
        
        try:
            db.create_collection("research_reports", validator=research_reports_validator)
            print("   Colección creada con validación")
        except CollectionInvalid:
            print("   Colección ya existe, actualizando validación...")
            db.command({
                "collMod": "research_reports",
                "validator": research_reports_validator
            })
        
        # Índices para research_reports
        print("   Creando índices...")
        db.research_reports.create_index([("report_id", ASCENDING)], unique=True)
        db.research_reports.create_index([("trial_id", ASCENDING)])
        db.research_reports.create_index([("fecha_reporte", DESCENDING)])
        db.research_reports.create_index([("investigador.id_usuario", ASCENDING)])
        db.research_reports.create_index([("tipo_reporte", ASCENDING)])
        print("   Índices creados")
        print()
        
        # coleccion: adverse_events
        print("4. Creando colección: adverse_events")
        
        adverse_events_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["event_id", "trial_id", "fecha_reporte", "severidad"],
                "properties": {
                    "event_id": {
                        "bsonType": "string",
                        "description": "Identificador único del evento"
                    },
                    "trial_id": {
                        "bsonType": "string",
                        "description": "ID del ensayo clínico"
                    },
                    "fecha_reporte": {
                        "bsonType": "date",
                        "description": "Fecha del evento"
                    },
                    "severidad": {
                        "enum": ["Leve", "Moderado", "Grave", "Crítico"],
                        "description": "Severidad del evento"
                    }
                }
            }
        }
        
        try:
            db.create_collection("adverse_events", validator=adverse_events_validator)
            print("   Colección creada con validación")
        except CollectionInvalid:
            print("   Colección ya existe, actualizando validación...")
            db.command({
                "collMod": "adverse_events",
                "validator": adverse_events_validator
            })
        
        # Índices para adverse_events
        print("   Creando índices...")
        db.adverse_events.create_index([("event_id", ASCENDING)], unique=True)
        db.adverse_events.create_index([("trial_id", ASCENDING)])
        db.adverse_events.create_index([("severidad", ASCENDING)])
        db.adverse_events.create_index([("fecha_reporte", DESCENDING)])
        print("   Índices creados")
        print()
    
        # coleccion: compound_interactions
        print("5. Creando colección: compound_interactions")
        
        compound_interactions_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["interaction_id", "compuesto_a", "compuesto_b", "tipo_interaccion", "severidad"],
                "properties": {
                    "interaction_id": {
                        "bsonType": "string",
                        "description": "Identificador único de la interacción"
                    },
                    "compuesto_a": {
                        "bsonType": "string",
                        "description": "Primer compuesto"
                    },
                    "compuesto_b": {
                        "bsonType": "string",
                        "description": "Segundo compuesto"
                    },
                    "tipo_interaccion": {
                        "enum": ["Sinérgica", "Antagónica", "Aditiva", "Potenciadora"],
                        "description": "Tipo de interacción"
                    },
                    "severidad": {
                        "enum": ["Leve", "Moderada", "Grave", "Contraindicada"],
                        "description": "Severidad de la interacción"
                    }
                }
            }
        }
        
        try:
            db.create_collection("compound_interactions", validator=compound_interactions_validator)
            print("   Colección creada con validación")
        except CollectionInvalid:
            print("   Colección ya existe, actualizando validación...")
            db.command({
                "collMod": "compound_interactions",
                "validator": compound_interactions_validator
            })
        
        # Índices para compound_interactions
        print("   Creando índices...")
        db.compound_interactions.create_index([("interaction_id", ASCENDING)], unique=True)
        db.compound_interactions.create_index([("compuesto_a", ASCENDING)])
        db.compound_interactions.create_index([("compuesto_b", ASCENDING)])
        db.compound_interactions.create_index([
            ("compuesto_a", ASCENDING),
            ("compuesto_b", ASCENDING)
        ], name="compound_pair_index")
        db.compound_interactions.create_index([("severidad", ASCENDING)])
        print("   Índices creados")
        print()
        
        # Crear usuario en la base de datos
        print("6. Configurando usuario de base de datos...")
        try:
            # Crear usuario en la base de datos admin
            admin_db = client.admin
            admin_db.command({
                "createUser": Config.MONGODB_CONFIG['username'],
                "pwd": Config.MONGODB_CONFIG['password'],
                "roles": [
                    {
                        "role": "readWrite",
                        "db": Config.MONGODB_CONFIG['database']
                    },
                    {
                        "role": "dbAdmin",
                        "db": Config.MONGODB_CONFIG['database']
                    }
                ]
            })
            print(f"   Usuario '{Config.MONGODB_CONFIG['username']}' creado")
        except OperationFailure as e:
            if "already exists" in str(e) or "already" in str(e).lower():
                print(f"   Usuario '{Config.MONGODB_CONFIG['username']}' ya existe")
            else:
                print(f"   Advertencia al crear usuario: {e}")
                print(f"   (Esto es normal si MongoDB no requiere autenticación)")
        print()
        
        print("=" * 60)
        print("CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        print()
        print("Colecciones creadas:")
        for collection_name in db.list_collection_names():
            count = db[collection_name].count_documents({})
            print(f"  - {collection_name}: {count} documentos")
        print()
        print("Siguiente paso: Ejecutar mongodb_seed.py para cargar datos iniciales")
        print()
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nVerifica que:")
        print("1. MongoDB esté instalado e iniciado")
        print("2. La configuración en config/config.py sea correcta")
        print("3. Tengas permisos para crear bases de datos")
        return False


if __name__ == "__main__":
    success = setup_mongodb()
    sys.exit(0 if success else 1)
