import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from datetime import datetime, timedelta
from config.config import Config

def seed_mongodb():
    # Cargar datos iniciales en MongoDB
    
    print("=" * 60)
    print("PHARMAFLOW SOLUTIONS - Datos Iniciales MongoDB")
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
        
        # Limpiar colecciones existentes (opcional)
        print("2. Limpiando datos existentes...")
        db.clinical_trials.delete_many({})
        db.research_reports.delete_many({})
        db.adverse_events.delete_many({})
        db.compound_interactions.delete_many({})
        print("   Colecciones limpiadas")
        print()
        
        #apartado de ensayos clinicos

        print("3. Insertando Ensayos Clínicos...")
        
        clinical_trials = [
            {
                "trial_id": "CT-2024-001",
                "titulo": "Eficacia y Seguridad de Nuevo Antibiótico de Amplio Espectro",
                "medicamento_id": 4,  # Amoxicilina (referencia a MySQL)
                "medicamento_nombre": "Amoxicilina 500mg",
                "principio_activo": "Amoxicilina",
                "fase": "Fase III",
                "fecha_inicio": datetime(2024, 1, 15),
                "fecha_finalizacion": None,
                "estado": "En Curso",
                "objetivo_principal": "Evaluar la eficacia y seguridad de una nueva formulación de amoxicilina en el tratamiento de infecciones respiratorias agudas en adultos",
                "poblacion_objetivo": {
                    "edad_minima": 18,
                    "edad_maxima": 65,
                    "sexo": "Ambos",
                    "criterios_inclusion": [
                        "Diagnóstico confirmado de infección respiratoria aguda",
                        "Sin alergias conocidas a penicilinas",
                        "Función renal normal"
                    ],
                    "criterios_exclusion": [
                        "Embarazo o lactancia",
                        "Uso de antibióticos en las últimas 2 semanas",
                        "Enfermedades crónicas descompensadas"
                    ]
                },
                "investigadores": [
                    {
                        "nombre": "Dra. Ana Martínez Sánchez",
                        "rol": "Investigador Principal",
                        "institucion": "Hospital General del Norte",
                        "email": "ana.martinez@pharmaflow.com"
                    },
                    {
                        "nombre": "Dr. Luis Hernández Torres",
                        "rol": "Co-Investigador",
                        "institucion": "Clínica Médica Familiar",
                        "email": "luis.hernandez@pharmaflow.com"
                    }
                ],
                "participantes": {
                    "objetivo": 200,
                    "reclutados": 145,
                    "completados": 87,
                    "abandonos": 12
                },
                "resultados_preliminares": {
                    "tasa_curacion": 89.5,
                    "tiempo_mejora_promedio_dias": 5.2,
                    "adherencia_tratamiento": 94.3,
                    "observaciones": "Los resultados preliminares muestran una eficacia superior al comparador en un 12%"
                },
                "efectos_secundarios": [
                    {
                        "sintoma": "Náuseas leves",
                        "frecuencia": "15%",
                        "severidad": "Leve"
                    },
                    {
                        "sintoma": "Diarrea",
                        "frecuencia": "8%",
                        "severidad": "Leve a Moderado"
                    },
                    {
                        "sintoma": "Erupciones cutáneas",
                        "frecuencia": "3%",
                        "severidad": "Moderado"
                    }
                ],
                "notas_investigacion": [
                    {
                        "fecha": datetime(2024, 2, 15),
                        "investigador": "Dra. Ana Martínez",
                        "nota": "Se observa mejor tolerancia en pacientes menores de 45 años. Considerar análisis por subgrupos."
                    },
                    {
                        "fecha": datetime(2024, 3, 20),
                        "investigador": "Dr. Luis Hernández",
                        "nota": "Tres pacientes reportaron efectos adversos gastrointestinales moderados. Se ha ajustado la dosis en protocolos futuros."
                    }
                ],
                "documentos_adjuntos": [
                    {
                        "tipo": "Protocolo",
                        "nombre": "Protocolo_CT-2024-001_v2.pdf",
                        "fecha_subida": datetime(2024, 1, 10)
                    },
                    {
                        "tipo": "Consentimiento Informado",
                        "nombre": "Consentimiento_CT-2024-001.pdf",
                        "fecha_subida": datetime(2024, 1, 10)
                    }
                ]
            },
            {
                "trial_id": "CT-2024-002",
                "titulo": "Estudio de Fase II - Ibuprofeno 800mg en Dolor Crónico",
                "medicamento_id": 1,  # Ibuprofeno (referencia a MySQL)
                "medicamento_nombre": "Ibuprofeno 800mg",
                "principio_activo": "Ibuprofeno",
                "fase": "Fase II",
                "fecha_inicio": datetime(2024, 3, 1),
                "fecha_finalizacion": None,
                "estado": "En Curso",
                "objetivo_principal": "Evaluar la eficacia analgésica de ibuprofeno 800mg en pacientes con dolor crónico musculoesquelético",
                "poblacion_objetivo": {
                    "edad_minima": 25,
                    "edad_maxima": 70,
                    "sexo": "Ambos",
                    "criterios_inclusion": [
                        "Dolor crónico musculoesquelético de al menos 3 meses",
                        "Escala de dolor EVA > 5",
                        "Sin contraindicaciones para AINEs"
                    ],
                    "criterios_exclusion": [
                        "Úlcera péptica activa",
                        "Insuficiencia renal",
                        "Embarazo"
                    ]
                },
                "investigadores": [
                    {
                        "nombre": "Dr. Carlos Ramírez Gómez",
                        "rol": "Investigador Principal",
                        "institucion": "Centro de Investigación del Dolor",
                        "email": "carlos.ramirez@pharmaflow.com"
                    }
                ],
                "participantes": {
                    "objetivo": 120,
                    "reclutados": 98,
                    "completados": 45,
                    "abandonos": 8
                },
                "resultados_preliminares": {
                    "reduccion_dolor_promedio": 42.5,
                    "tiempo_inicio_efecto_minutos": 45,
                    "duracion_efecto_horas": 6.8,
                    "observaciones": "Buena respuesta en el 78% de los pacientes"
                },
                "efectos_secundarios": [
                    {
                        "sintoma": "Molestias gástricas",
                        "frecuencia": "22%",
                        "severidad": "Leve"
                    },
                    {
                        "sintoma": "Cefalea",
                        "frecuencia": "5%",
                        "severidad": "Leve"
                    }
                ],
                "notas_investigacion": [
                    {
                        "fecha": datetime(2024, 4, 10),
                        "investigador": "Dr. Carlos Ramírez",
                        "nota": "Se observa mejor respuesta cuando se administra con alimentos."
                    }
                ],
                "documentos_adjuntos": []
            },
            {
                "trial_id": "CT-2023-005",
                "titulo": "Paracetamol en Tratamiento de Fiebre Pediátrica",
                "medicamento_id": 2,  # Paracetamol (referencia a MySQL)
                "medicamento_nombre": "Paracetamol 500mg",
                "principio_activo": "Paracetamol",
                "fase": "Fase IV",
                "fecha_inicio": datetime(2023, 6, 1),
                "fecha_finalizacion": datetime(2024, 5, 30),
                "estado": "Completado",
                "objetivo_principal": "Estudio post-comercialización de seguridad en población pediátrica",
                "poblacion_objetivo": {
                    "edad_minima": 2,
                    "edad_maxima": 12,
                    "sexo": "Ambos",
                    "criterios_inclusion": [
                        "Fiebre > 38.5°C",
                        "Peso adecuado para la edad",
                        "Consentimiento de padres/tutores"
                    ],
                    "criterios_exclusion": [
                        "Hepatopatía conocida",
                        "Alergias al paracetamol"
                    ]
                },
                "investigadores": [
                    {
                        "nombre": "Dra. Patricia López Vega",
                        "rol": "Investigador Principal",
                        "institucion": "Hospital Infantil Central",
                        "email": "patricia.lopez@pharmaflow.com"
                    }
                ],
                "participantes": {
                    "objetivo": 300,
                    "reclutados": 315,
                    "completados": 298,
                    "abandonos": 17
                },
                "resultados_preliminares": {
                    "tasa_reduccion_fiebre": 96.2,
                    "tiempo_hasta_normalizacion_horas": 3.5,
                    "eventos_adversos_graves": 0,
                    "observaciones": "Perfil de seguridad excelente confirmado en población pediátrica"
                },
                "efectos_secundarios": [
                    {
                        "sintoma": "Náuseas leves",
                        "frecuencia": "4%",
                        "severidad": "Leve"
                    }
                ],
                "notas_investigacion": [
                    {
                        "fecha": datetime(2024, 5, 15),
                        "investigador": "Dra. Patricia López",
                        "nota": "Estudio completado exitosamente. Datos confirman perfil de seguridad establecido."
                    }
                ],
                "documentos_adjuntos": [
                    {
                        "tipo": "Reporte Final",
                        "nombre": "Reporte_Final_CT-2023-005.pdf",
                        "fecha_subida": datetime(2024, 6, 1)
                    }
                ]
            }
        ]
        
        result = db.clinical_trials.insert_many(clinical_trials)
        print(f"   {len(result.inserted_ids)} ensayos clínicos insertados")
        print()
        
        # REPORTES DE INVESTIGACIÓN
        print("4. Insertando Reportes de Investigación...")
        
        research_reports = [
            {
                "report_id": "RPT-2024-001",
                "trial_id": "CT-2024-001",
                "fecha_reporte": datetime(2024, 6, 15),
                "investigador": {
                    "nombre": "Dra. Ana Martínez Sánchez",
                    "id_usuario": 3
                },
                "tipo_reporte": "Intermedio",
                "periodo_evaluacion": {
                    "inicio": datetime(2024, 1, 15),
                    "fin": datetime(2024, 6, 15)
                },
                "resumen_ejecutivo": "Análisis intermedio a los 6 meses muestra resultados prometedores con buena tolerancia.",
                "hallazgos_principales": [
                    "Tasa de curación del 89.5% en población analizada",
                    "Efectos adversos principalmente leves y transitorios",
                    "Alta adherencia al tratamiento (94.3%)"
                ],
                "estadisticas": {
                    "total_participantes": 145,
                    "completaron_seguimiento": 87,
                    "eventos_adversos": 23,
                    "eventos_adversos_graves": 0
                },
                "conclusiones": "Los datos intermedios apoyan la continuación del estudio hasta su finalización planificada.",
                "recomendaciones": [
                    "Continuar monitoreo de efectos gastrointestinales",
                    "Aumentar frecuencia de visitas para pacientes >60 años"
                ]
            },
            {
                "report_id": "RPT-2024-002",
                "trial_id": "CT-2024-002",
                "fecha_reporte": datetime(2024, 5, 20),
                "investigador": {
                    "nombre": "Dr. Carlos Ramírez Gómez",
                    "id_usuario": 3
                },
                "tipo_reporte": "Seguimiento",
                "periodo_evaluacion": {
                    "inicio": datetime(2024, 3, 1),
                    "fin": datetime(2024, 5, 20)
                },
                "resumen_ejecutivo": "Reporte de seguimiento del primer trimestre del estudio de dolor crónico.",
                "hallazgos_principales": [
                    "Reducción promedio del dolor del 42.5%",
                    "Mejor respuesta cuando se administra con alimentos",
                    "22% reportó molestias gástricas leves"
                ],
                "estadisticas": {
                    "total_participantes": 98,
                    "completaron_seguimiento": 45,
                    "eventos_adversos": 19,
                    "eventos_adversos_graves": 0
                },
                "conclusiones": "Resultados preliminares positivos. Reclutamiento progresa adecuadamente.",
                "recomendaciones": [
                    "Recomendar administración con alimentos en próximas visitas",
                    "Evaluar necesidad de tratamiento gastroprotector en pacientes de riesgo"
                ]
            }
        ]
        
        result = db.research_reports.insert_many(research_reports)
        print(f"   {len(result.inserted_ids)} reportes insertados")
        print()
        
        # ============================================
        # EVENTOS ADVERSOS
        # ============================================
        print("5. Insertando Eventos Adversos...")
        
        adverse_events = [
            {
                "event_id": "AE-2024-001",
                "trial_id": "CT-2024-001",
                "paciente_id": "P-001",
                "fecha_reporte": datetime(2024, 2, 20),
                "fecha_evento": datetime(2024, 2, 18),
                "descripcion": "Paciente presentó erupciones cutáneas en brazos y torso 3 días después de iniciar tratamiento",
                "severidad": "Moderado",
                "relacionado_medicamento": True,
                "accion_tomada": "Suspensión temporal del tratamiento, administración de antihistamínicos",
                "desenlace": "Resuelto",
                "fecha_resolucion": datetime(2024, 2, 25),
                "reportado_por": "Dra. Ana Martínez Sánchez"
            },
            {
                "event_id": "AE-2024-002",
                "trial_id": "CT-2024-001",
                "paciente_id": "P-045",
                "fecha_reporte": datetime(2024, 3, 15),
                "fecha_evento": datetime(2024, 3, 14),
                "descripcion": "Diarrea moderada y náuseas persistentes",
                "severidad": "Leve",
                "relacionado_medicamento": True,
                "accion_tomada": "Ajuste de dosis, hidratación oral",
                "desenlace": "Resuelto",
                "fecha_resolucion": datetime(2024, 3, 18),
                "reportado_por": "Dr. Luis Hernández Torres"
            },
            {
                "event_id": "AE-2024-003",
                "trial_id": "CT-2024-002",
                "paciente_id": "P-023",
                "fecha_reporte": datetime(2024, 4, 5),
                "fecha_evento": datetime(2024, 4, 3),
                "descripcion": "Dolor epigástrico intenso después de tomar medicamento",
                "severidad": "Moderado",
                "relacionado_medicamento": True,
                "accion_tomada": "Suspensión del medicamento, prescripción de omeprazol",
                "desenlace": "Resuelto",
                "fecha_resolucion": datetime(2024, 4, 10),
                "reportado_por": "Dr. Carlos Ramírez Gómez"
            }
        ]
        
        result = db.adverse_events.insert_many(adverse_events)
        print(f"   {len(result.inserted_ids)} eventos adversos insertados")
        print()
        
        # ============================================
        # INTERACCIONES DE COMPUESTOS
        # ============================================
        print("6. Insertando Interacciones de Compuestos...")
        
        compound_interactions = [
            {
                "interaction_id": "INT-001",
                "compuesto_a": "Ibuprofeno",
                "compuesto_b": "Warfarina",
                "tipo_interaccion": "Antagónica",
                "severidad": "Grave",
                "mecanismo": "El ibuprofeno puede disminuir el efecto anticoagulante de la warfarina y aumentar riesgo de sangrado gastrointestinal",
                "recomendaciones": "Evitar uso concomitante. Si es necesario, monitorear INR de cerca.",
                "referencias_cientificas": [
                    "J Clin Pharmacol. 2020;60(3):345-352",
                    "Br J Clin Pharmacol. 2019;85(8):1689-1697"
                ],
                "fecha_actualizacion": datetime(2024, 1, 10)
            },
            {
                "interaction_id": "INT-002",
                "compuesto_a": "Paracetamol",
                "compuesto_b": "Alcohol",
                "tipo_interaccion": "Potenciadora",
                "severidad": "Grave",
                "mecanismo": "El consumo crónico de alcohol puede aumentar hepatotoxicidad del paracetamol",
                "recomendaciones": "Evitar consumo de alcohol durante tratamiento con paracetamol. Dosis máxima reducida en pacientes con consumo crónico de alcohol.",
                "referencias_cientificas": [
                    "Hepatology. 2021;73(2):567-580",
                    "Clin Liver Dis. 2020;15(3):345-358"
                ],
                "fecha_actualizacion": datetime(2024, 1, 15)
            },
            {
                "interaction_id": "INT-003",
                "compuesto_a": "Amoxicilina",
                "compuesto_b": "Anticonceptivos Orales",
                "tipo_interaccion": "Antagónica",
                "severidad": "Moderada",
                "mecanismo": "Los antibióticos pueden disminuir la eficacia de anticonceptivos orales al alterar flora intestinal",
                "recomendaciones": "Recomendar métodos anticonceptivos adicionales durante tratamiento y 7 días después.",
                "referencias_cientificas": [
                    "Contraception. 2019;99(4):224-231"
                ],
                "fecha_actualizacion": datetime(2024, 2, 1)
            },
            {
                "interaction_id": "INT-004",
                "compuesto_a": "Ibuprofeno",
                "compuesto_b": "Aspirina",
                "tipo_interaccion": "Antagónica",
                "severidad": "Moderada",
                "mecanismo": "El ibuprofeno puede reducir el efecto cardioprotector de la aspirina",
                "recomendaciones": "Si ambos son necesarios, administrar aspirina al menos 2 horas antes del ibuprofeno.",
                "referencias_cientificas": [
                    "Circulation. 2020;142(12):1144-1154"
                ],
                "fecha_actualizacion": datetime(2024, 2, 10)
            },
            {
                "interaction_id": "INT-005",
                "compuesto_a": "Amoxicilina",
                "compuesto_b": "Metotrexato",
                "tipo_interaccion": "Potenciadora",
                "severidad": "Grave",
                "mecanismo": "La amoxicilina puede disminuir la excreción renal de metotrexato, aumentando su toxicidad",
                "recomendaciones": "Evitar uso concomitante. Si es necesario, monitorear niveles de metotrexato.",
                "referencias_cientificas": [
                    "J Rheumatol. 2019;46(8):891-897"
                ],
                "fecha_actualizacion": datetime(2024, 3, 1)
            }
        ]
        
        result = db.compound_interactions.insert_many(compound_interactions)
        print(f"   {len(result.inserted_ids)} interacciones insertadas")
        print()
        
        # ============================================
        # RESUMEN FINAL
        # ============================================
        print("=" * 60)
        print("DATOS INICIALES CARGADOS EXITOSAMENTE")
        print("=" * 60)
        print()
        print("Resumen de datos insertados:")
        print(f"  - Ensayos Clínicos: {db.clinical_trials.count_documents({})}")
        print(f"  - Reportes de Investigación: {db.research_reports.count_documents({})}")
        print(f"  - Eventos Adversos: {db.adverse_events.count_documents({})}")
        print(f"  - Interacciones de Compuestos: {db.compound_interactions.count_documents({})}")
        print()
        print("Base de datos lista para usar")
        print()
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nVerifica que:")
        print("1. MongoDB esté instalado e iniciado")
        print("2. Hayas ejecutado mongodb_setup.py primero")
        print("3. La configuración en config/config.py sea correcta")
        return False


if __name__ == "__main__":
    success = seed_mongodb()
    sys.exit(0 if success else 1)
