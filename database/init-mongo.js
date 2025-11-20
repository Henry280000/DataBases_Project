// Script de inicialización para MongoDB
db = db.getSiblingDB('pharmaflow_nosql');

// Crear colecciones
db.createCollection('ensayos_clinicos');
db.createCollection('eventos_adversos');
db.createCollection('reportes_investigacion');
db.createCollection('interacciones_compuestos');

// Insertar datos de prueba en ensayos_clinicos
db.ensayos_clinicos.insertMany([
    {
        codigo_ensayo: "EC2024001",
        titulo: "Estudio de Eficacia de Amoxicilina en Infecciones Respiratorias",
        fecha_inicio: new Date("2024-01-15"),
        fecha_fin_estimada: new Date("2025-06-30"),
        fase: "III",
        estado: "Activo",
        medicamento: {
            nombre: "Amoxicilina",
            dosis: "500mg",
            forma: "Tableta"
        },
        investigador_principal: {
            nombre: "Dr. Carlos Mendoza",
            especialidad: "Infectología",
            institucion: "Hospital Central"
        },
        participantes: {
            total: 150,
            completados: 45,
            activos: 100,
            retirados: 5
        },
        criterios_inclusion: [
            "Edad entre 18 y 65 años",
            "Diagnóstico confirmado de infección respiratoria",
            "Sin alergias a betalactámicos"
        ],
        objetivos_primarios: "Evaluar eficacia del medicamento en tratamiento de infecciones respiratorias",
        creado_en: new Date()
    },
    {
        codigo_ensayo: "EC2024002",
        titulo: "Evaluación de Seguridad de Ibuprofeno en Pacientes Geriátricos",
        fecha_inicio: new Date("2024-02-01"),
        fecha_fin_estimada: new Date("2025-08-31"),
        fase: "IV",
        estado: "Activo",
        medicamento: {
            nombre: "Ibuprofeno",
            dosis: "400mg",
            forma: "Tableta"
        },
        investigador_principal: {
            nombre: "Dra. Ana Torres",
            especialidad: "Geriatría",
            institucion: "Instituto Geriátrico Nacional"
        },
        participantes: {
            total: 200,
            completados: 120,
            activos: 70,
            retirados: 10
        },
        criterios_inclusion: [
            "Edad mayor a 65 años",
            "Función renal normal",
            "Sin historial de úlcera gástrica"
        ],
        objetivos_primarios: "Evaluar seguridad y tolerabilidad en población geriátrica",
        creado_en: new Date()
    },
    {
        codigo_ensayo: "EC2024003",
        titulo: "Estudio de Omeprazol en Tratamiento de Reflujo Gastroesofágico",
        fecha_inicio: new Date("2024-03-10"),
        fecha_fin_estimada: new Date("2025-09-30"),
        fase: "III",
        estado: "Reclutando",
        medicamento: {
            nombre: "Omeprazol",
            dosis: "20mg",
            forma: "Cápsula"
        },
        investigador_principal: {
            nombre: "Dr. Roberto Díaz",
            especialidad: "Gastroenterología",
            institucion: "Centro Médico Digestivo"
        },
        participantes: {
            total: 180,
            completados: 30,
            activos: 140,
            retirados: 10
        },
        criterios_inclusion: [
            "Diagnóstico de ERGE confirmado",
            "Edad entre 25 y 70 años",
            "Sin tratamiento previo con IBP"
        ],
        objetivos_primarios: "Determinar eficacia en control de síntomas de reflujo",
        creado_en: new Date()
    }
]);

// Insertar eventos adversos
db.eventos_adversos.insertMany([
    {
        id_evento: "EA001",
        codigo_ensayo: "EC2024001",
        fecha_reporte: new Date("2024-03-10"),
        severidad: "Leve",
        descripcion: "Náuseas leves después de la administración",
        paciente_id: "P001",
        medidas_tomadas: "Reducción temporal de dosis",
        resuelto: true,
        fecha_resolucion: new Date("2024-03-12")
    },
    {
        id_evento: "EA002",
        codigo_ensayo: "EC2024001",
        fecha_reporte: new Date("2024-04-15"),
        severidad: "Moderado",
        descripcion: "Reacción alérgica cutánea",
        paciente_id: "P045",
        medidas_tomadas: "Suspensión del tratamiento y antihistamínicos",
        resuelto: true,
        fecha_resolucion: new Date("2024-04-18")
    },
    {
        id_evento: "EA003",
        codigo_ensayo: "EC2024002",
        fecha_reporte: new Date("2024-05-20"),
        severidad: "Leve",
        descripcion: "Dolor estomacal leve",
        paciente_id: "P112",
        medidas_tomadas: "Tomar con alimentos",
        resuelto: true,
        fecha_resolucion: new Date("2024-05-21")
    }
]);

// Insertar reportes de investigación
db.reportes_investigacion.insertMany([
    {
        id_reporte: "RI001",
        codigo_ensayo: "EC2024001",
        fecha_reporte: new Date("2024-03-01"),
        tipo: "Reporte Trimestral",
        periodo: "Q1 2024",
        resultados_preliminares: "Tasa de eficacia del 85% en el grupo de tratamiento vs 45% en placebo",
        conclusiones: "Resultados prometedores, continuar según protocolo",
        eventos_adversos_reportados: 2,
        abandonos: 5
    },
    {
        id_reporte: "RI002",
        codigo_ensayo: "EC2024002",
        fecha_reporte: new Date("2024-04-15"),
        tipo: "Reporte Semestral",
        periodo: "S1 2024",
        resultados_preliminares: "Buena tolerabilidad en población geriátrica con eventos adversos mínimos",
        conclusiones: "Perfil de seguridad aceptable para la población objetivo",
        eventos_adversos_reportados: 1,
        abandonos: 10
    }
]);

// Insertar interacciones de compuestos
db.interacciones_compuestos.insertMany([
    {
        compuesto_a: "Amoxicilina",
        compuesto_b: "Ácido Clavulánico",
        tipo_interaccion: "Sinérgica",
        nivel_severidad: "Beneficiosa",
        descripcion: "Potenciación del efecto antibacteriano, el ácido clavulánico inhibe betalactamasas",
        recomendaciones: "Combinación terapéutica recomendada para mayor espectro",
        referencias_bibliograficas: ["J Antimicrob Chemother 2020;75:1-10"]
    },
    {
        compuesto_a: "Ibuprofeno",
        compuesto_b: "Omeprazol",
        tipo_interaccion: "Protectora",
        nivel_severidad: "Beneficiosa",
        descripcion: "Omeprazol reduce el riesgo de efectos gastrointestinales del ibuprofeno",
        recomendaciones: "Considerar gastroprotección en uso prolongado de AINE",
        referencias_bibliograficas: ["Aliment Pharmacol Ther 2019;49:1415-1424"]
    },
    {
        compuesto_a: "Ibuprofeno",
        compuesto_b: "Aspirina",
        tipo_interaccion: "Antagonista",
        nivel_severidad: "Moderada",
        descripcion: "Ibuprofeno puede reducir el efecto antiagregante de la aspirina",
        recomendaciones: "Evitar uso concomitante o espaciar administración",
        referencias_bibliograficas: ["Circulation 2020;141:e60-e88"]
    }
]);

print('Base de datos MongoDB inicializada con éxito');
print('Colecciones creadas: ' + db.getCollectionNames().length);
print('Ensayos clínicos: ' + db.ensayos_clinicos.count());
print('Eventos adversos: ' + db.eventos_adversos.count());
print('Reportes: ' + db.reportes_investigacion.count());
print('Interacciones: ' + db.interacciones_compuestos.count());
