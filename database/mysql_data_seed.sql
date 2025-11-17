USE pharmaflow_relational;


-- Usuarios del Sistema
INSERT INTO usuarios (username, password_hash, nombre_completo, email, telefono, rol, activo) VALUES
('admin_gerente', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lH4vzXvNQZJa', 'Carlos Mendoza Ruiz', 'carlos.mendoza@pharmaflow.com', '5551234567', 'Gerente', TRUE),
('maria_farm', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lH4vzXvNQZJa', 'María García López', 'maria.garcia@pharmaflow.com', '5552345678', 'Farmacéutico', TRUE),
('jose_farm', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lH4vzXvNQZJa', 'José Rodríguez Pérez', 'jose.rodriguez@pharmaflow.com', '5553456789', 'Farmacéutico', TRUE),
('ana_investigadora', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lH4vzXvNQZJa', 'Ana Martínez Sánchez', 'ana.martinez@pharmaflow.com', '5554567890', 'Investigador', TRUE),
('luis_investigador', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lH4vzXvNQZJa', 'Luis Hernández Torres', 'luis.hernandez@pharmaflow.com', '5555678901', 'Investigador', TRUE);

-- tipos de medicmanetos
INSERT INTO categorias (nombre, descripcion) VALUES
('Analgésicos', 'Medicamentos para aliviar el dolor'),
('Antibióticos', 'Medicamentos para combatir infecciones bacterianas'),
('Antiinflamatorios', 'Medicamentos para reducir la inflamación'),
('Antihistamínicos', 'Medicamentos para alergias'),
('Antihipertensivos', 'Medicamentos para controlar la presión arterial'),
('Antidiabéticos', 'Medicamentos para controlar la diabetes'),
('Antiácidos', 'Medicamentos para problemas gastrointestinales'),
('Vitaminas y Suplementos', 'Complementos nutricionales');

-- medicamnetos
INSERT INTO medicamentos (nombre, principio_activo, id_categoria, descripcion, indicaciones, contraindicaciones, dosis_recomendada) VALUES
-- Analgésicos
('Paracetamol 500mg', 'Paracetamol', 1, 'Analgésico y antipirético', 'Dolor leve a moderado, fiebre', 'Hipersensibilidad al paracetamol, insuficiencia hepática grave', '500mg cada 6-8 horas'),
('Ibuprofeno 400mg', 'Ibuprofeno', 1, 'Analgésico, antipirético y antiinflamatorio', 'Dolor, fiebre, inflamación', 'Úlcera péptica activa, insuficiencia renal grave', '400mg cada 6-8 horas'),
('Ketorolaco 10mg', 'Ketorolaco', 1, 'Analgésico potente', 'Dolor moderado a severo', 'Úlcera péptica, embarazo, insuficiencia renal', '10mg cada 4-6 horas'),

-- Antibióticos
('Amoxicilina 500mg', 'Amoxicilina', 2, 'Antibiótico de amplio espectro', 'Infecciones bacterianas', 'Alergia a penicilinas', '500mg cada 8 horas'),
('Azitromicina 500mg', 'Azitromicina', 2, 'Antibiótico macrólido', 'Infecciones respiratorias, piel', 'Hipersensibilidad a macrólidos', '500mg día 1, luego 250mg días 2-5'),
('Ciprofloxacino 500mg', 'Ciprofloxacino', 2, 'Antibiótico quinolona', 'Infecciones urinarias, respiratorias', 'Embarazo, menores de 18 años', '500mg cada 12 horas'),

-- Antiinflamatorios
('Naproxeno 250mg', 'Naproxeno', 3, 'Antiinflamatorio no esteroideo', 'Dolor, inflamación, artritis', 'Úlcera péptica, insuficiencia renal', '250mg cada 6-8 horas'),
('Diclofenaco 50mg', 'Diclofenaco', 3, 'Antiinflamatorio potente', 'Dolor, inflamación aguda', 'Hipersensibilidad a AINEs', '50mg cada 8 horas'),

-- Antihistamínicos
('Loratadina 10mg', 'Loratadina', 4, 'Antihistamínico no sedante', 'Alergias, rinitis', 'Hipersensibilidad conocida', '10mg una vez al día'),
('Cetirizina 10mg', 'Cetirizina', 4, 'Antihistamínico de segunda generación', 'Alergias estacionales', 'Insuficiencia renal grave', '10mg una vez al día'),

-- Antihipertensivos
('Losartán 50mg', 'Losartán', 5, 'Antagonista de receptores de angiotensina II', 'Hipertensión arterial', 'Embarazo, hiperpotasemia', '50mg una vez al día'),
('Enalapril 10mg', 'Enalapril', 5, 'Inhibidor de la ECA', 'Hipertensión, insuficiencia cardíaca', 'Embarazo, angioedema', '10mg una o dos veces al día'),

-- Antidiabéticos
('Metformina 850mg', 'Metformina', 6, 'Antidiabético oral', 'Diabetes tipo 2', 'Insuficiencia renal, acidosis', '850mg con las comidas'),
('Glibenclamida 5mg', 'Glibenclamida', 6, 'Sulfonilurea', 'Diabetes tipo 2', 'Diabetes tipo 1, embarazo', '5mg antes del desayuno'),

-- Antiácidos
('Omeprazol 20mg', 'Omeprazol', 7, 'Inhibidor de bomba de protones', 'Úlcera, reflujo gastroesofágico', 'Hipersensibilidad conocida', '20mg una vez al día'),
('Ranitidina 150mg', 'Ranitidina', 7, 'Antagonista H2', 'Úlcera, acidez', 'Insuficiencia renal grave', '150mg dos veces al día'),

-- Vitaminas
('Complejo B', 'Vitaminas B1, B6, B12', 8, 'Suplemento vitamínico', 'Deficiencias vitamínicas', 'Hipersensibilidad', '1 tableta al día'),
('Vitamina C 1000mg', 'Ácido ascórbico', 8, 'Antioxidante', 'Reforzar sistema inmune', 'Cálculos renales', '1000mg al día');

-- proveedores
INSERT INTO proveedores (nombre, rfc, telefono, email, direccion, contacto_principal, activo) VALUES
('Distribuidora Farmacéutica del Centro', 'DFC980123ABC', '5556789012', 'ventas@dfcentro.com', 'Av. Insurgentes 1234, CDMX', 'Roberto Flores', TRUE),
('Laboratorios Nacionales S.A.', 'LNA850615XYZ', '5557890123', 'contacto@labnacionales.com', 'Calle Reforma 567, Monterrey', 'Patricia Gómez', TRUE),
('Pharma Import México', 'PIM920312QRS', '5558901234', 'info@pharmaimport.mx', 'Blvd. Constitución 890, Guadalajara', 'Miguel Ángel Ruiz', TRUE),
('Suministros Médicos Integrales', 'SMI870920MNO', '5559012345', 'compras@suministrosmedicos.com', 'Av. Juárez 345, Puebla', 'Laura Sánchez', TRUE);

-- lotes del inventario
INSERT INTO lotes (codigo_lote, id_medicamento, cantidad_inicial, cantidad_actual, precio_unitario, fecha_fabricacion, fecha_caducidad, ubicacion_almacen, estado) VALUES
-- Paracetamol
('LOT-PAR-2024-001', 1, 1000, 1000, 5.50, '2024-01-15', '2026-01-15', 'A-01-01', 'Disponible'),
('LOT-PAR-2024-002', 1, 1500, 1500, 5.30, '2024-03-20', '2026-03-20', 'A-01-02', 'Disponible'),

-- Ibuprofeno
('LOT-IBU-2024-001', 2, 800, 800, 8.75, '2024-02-10', '2026-02-10', 'A-02-01', 'Disponible'),
('LOT-IBU-2024-002', 2, 1200, 1200, 8.50, '2024-04-15', '2026-04-15', 'A-02-02', 'Disponible'),

-- Ketorolaco
('LOT-KET-2024-001', 3, 500, 500, 12.00, '2024-01-20', '2026-01-20', 'A-03-01', 'Disponible'),

-- Amoxicilina
('LOT-AMO-2024-001', 4, 2000, 2000, 15.50, '2024-02-05', '2025-08-05', 'B-01-01', 'Disponible'),
('LOT-AMO-2024-002', 4, 1800, 1800, 15.20, '2024-05-10', '2025-11-10', 'B-01-02', 'Disponible'),

-- Azitromicina
('LOT-AZI-2024-001', 5, 600, 600, 45.00, '2024-03-15', '2026-03-15', 'B-02-01', 'Disponible'),

-- Ciprofloxacino
('LOT-CIP-2024-001', 6, 800, 800, 25.50, '2024-02-20', '2026-02-20', 'B-03-01', 'Disponible'),

-- Naproxeno
('LOT-NAP-2024-001', 7, 900, 900, 10.00, '2024-01-25', '2026-01-25', 'A-04-01', 'Disponible'),

-- Diclofenaco
('LOT-DIC-2024-001', 8, 700, 700, 11.50, '2024-03-01', '2026-03-01', 'A-05-01', 'Disponible'),

-- Loratadina
('LOT-LOR-2024-001', 9, 1500, 1500, 6.50, '2024-02-15', '2026-02-15', 'C-01-01', 'Disponible'),

-- Cetirizina
('LOT-CET-2024-001', 10, 1300, 1300, 7.00, '2024-03-10', '2026-03-10', 'C-02-01', 'Disponible'),

-- Losartán
('LOT-LOS-2024-001', 11, 1000, 1000, 18.00, '2024-01-30', '2026-01-30', 'D-01-01', 'Disponible'),

-- Enalapril
('LOT-ENA-2024-001', 12, 950, 950, 16.50, '2024-02-25', '2026-02-25', 'D-02-01', 'Disponible'),

-- Metformina
('LOT-MET-2024-001', 13, 2500, 2500, 9.00, '2024-03-05', '2026-03-05', 'D-03-01', 'Disponible'),

-- Glibenclamida
('LOT-GLI-2024-001', 14, 800, 800, 12.50, '2024-02-10', '2026-02-10', 'D-04-01', 'Disponible'),

-- Omeprazol
('LOT-OME-2024-001', 15, 1800, 1800, 14.00, '2024-01-20', '2026-01-20', 'E-01-01', 'Disponible'),

-- Ranitidina
('LOT-RAN-2024-001', 16, 1200, 1200, 10.50, '2024-03-12', '2026-03-12', 'E-02-01', 'Disponible'),

-- Complejo B
('LOT-CPB-2024-001', 17, 2000, 2000, 8.00, '2024-02-18', '2026-02-18', 'F-01-01', 'Disponible'),

-- Vitamina C
('LOT-VTC-2024-001', 18, 1500, 1500, 12.00, '2024-03-20', '2026-03-20', 'F-02-01', 'Disponible');

-- clinetes
INSERT INTO clientes (nombre, tipo, rfc, telefono, email, direccion) VALUES
('Farmacia San Rafael', 'Farmacia', 'FSR910825ABC', '5550123456', 'farmacia@sanrafael.com', 'Calle Morelos 123, CDMX'),
('Hospital General del Norte', 'Hospital', 'HGN880515XYZ', '5551234567', 'compras@hospitalnorte.com', 'Av. Revolución 456, Monterrey'),
('Clínica Médica Familiar', 'Clínica', 'CMF930720QRS', '5552345678', 'administracion@clinicafamiliar.com', 'Blvd. Juárez 789, Guadalajara'),
('Juan Pérez Martínez', 'Persona', 'PEMJ850312ABC', '5553456789', 'juan.perez@email.com', 'Calle Hidalgo 234, CDMX'),
('María González López', 'Persona', 'GOLM920615XYZ', '5554567890', 'maria.gonzalez@email.com', 'Av. Reforma 567, Puebla'),
('Farmacia del Ahorro Centro', 'Farmacia', 'FAC950820MNO', '5555678901', 'centro@farmaciadelahorro.com', 'Calle Madero 890, CDMX');

-- ÓRDENES DE COMPRA
INSERT INTO ordenes_compra (numero_orden, id_proveedor, fecha_orden, fecha_entrega_esperada, fecha_entrega_real, estado, total, observaciones) VALUES
('OC-2024-001', 1, '2024-01-10', '2024-01-20', '2024-01-18', 'Recibida', 87500.00, 'Primera orden del año'),
('OC-2024-002', 2, '2024-02-05', '2024-02-15', '2024-02-15', 'Recibida', 125300.00, 'Orden de antibióticos'),
('OC-2024-003', 3, '2024-03-12', '2024-03-22', NULL, 'Aprobada', 95600.00, 'Pendiente de entrega');

-- Detalles de OC-2024-001
INSERT INTO detalles_orden_compra (id_orden_compra, id_medicamento, cantidad, precio_unitario) VALUES
(1, 1, 2500, 5.00),  -- Paracetamol
(1, 2, 2000, 8.00),  -- Ibuprofeno
(1, 9, 1500, 6.00),  -- Loratadina
(1, 17, 2000, 7.50); -- Complejo B

-- Detalles de OC-2024-002
INSERT INTO detalles_orden_compra (id_orden_compra, id_medicamento, cantidad, precio_unitario) VALUES
(2, 4, 3800, 14.50), -- Amoxicilina
(2, 5, 600, 42.00),  -- Azitromicina
(2, 6, 800, 24.00);  -- Ciprofloxacino

-- Detalles de OC-2024-003
INSERT INTO detalles_orden_compra (id_orden_compra, id_medicamento, cantidad, precio_unitario) VALUES
(3, 11, 1000, 17.00), -- Losartán
(3, 13, 2500, 8.50),  -- Metformina
(3, 15, 1800, 13.00); -- Omeprazol


SELECT 'Datos iniciales cargados exitosamente' AS mensaje,
       (SELECT COUNT(*) FROM usuarios) AS total_usuarios,
       (SELECT COUNT(*) FROM medicamentos) AS total_medicamentos,
       (SELECT COUNT(*) FROM lotes) AS total_lotes,
       (SELECT COUNT(*) FROM proveedores) AS total_proveedores,
       (SELECT COUNT(*) FROM clientes) AS total_clientes;
