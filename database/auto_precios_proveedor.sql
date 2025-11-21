USE pharmaflow_relational;

-- 1. TRIGGER: Crear precios automáticamente para nuevos medicamentos
DROP TRIGGER IF EXISTS after_medicamento_insert;

DELIMITER $$
CREATE DEFINER=CURRENT_USER TRIGGER after_medicamento_insert
AFTER INSERT ON medicamentos
FOR EACH ROW
BEGIN
    -- Insertar precio para cada proveedor activo
    INSERT INTO precios_proveedor (
        id_proveedor,
        id_medicamento,
        precio_base,
        cantidad_minima_descuento,
        porcentaje_descuento,
        fecha_vigencia_inicio,
        estado
    )
    SELECT 
        p.id_proveedor,
        NEW.id_medicamento,
        50.00,  -- Precio base por defecto
        30,     -- Cantidad mínima para descuento
        5.00,   -- 5% de descuento por defecto
        CURDATE(),
        'Activo'
    FROM proveedores p
    WHERE p.activo = TRUE;
END$$
DELIMITER ;

-- 2. PROCEDIMIENTO: Sincronizar medicamentos existentes sin precios
DROP PROCEDURE IF EXISTS sincronizar_precios_medicamentos;

DELIMITER $$
CREATE DEFINER=CURRENT_USER PROCEDURE sincronizar_precios_medicamentos()
BEGIN
    DECLARE medicamentos_agregados INT DEFAULT 0;
    
    -- Insertar precios para medicamentos que no tienen precios configurados
    INSERT INTO precios_proveedor (
        id_proveedor,
        id_medicamento,
        precio_base,
        cantidad_minima_descuento,
        porcentaje_descuento,
        fecha_vigencia_inicio,
        estado
    )
    SELECT 
        p.id_proveedor,
        m.id_medicamento,
        50.00,  -- Precio base por defecto
        30,     -- Cantidad mínima para descuento
        5.00,   -- 5% de descuento por defecto
        CURDATE(),
        'Activo'
    FROM medicamentos m
    CROSS JOIN proveedores p
    WHERE p.activo = TRUE
    AND NOT EXISTS (
        SELECT 1 
        FROM precios_proveedor pp 
        WHERE pp.id_medicamento = m.id_medicamento 
        AND pp.id_proveedor = p.id_proveedor
        AND pp.estado = 'Activo'
    );
    
    SET medicamentos_agregados = ROW_COUNT();
    
    SELECT 
        medicamentos_agregados AS registros_creados,
        'Sincronización completada' AS mensaje;
END$$
DELIMITER ;

-- 3. PROCEDIMIENTO: Agregar nuevo medicamento con precios
DROP PROCEDURE IF EXISTS agregar_medicamento_con_precios;

DELIMITER $$
CREATE DEFINER=CURRENT_USER PROCEDURE agregar_medicamento_con_precios(
    IN p_nombre VARCHAR(200),
    IN p_principio_activo VARCHAR(200),
    IN p_id_categoria INT,
    IN p_descripcion TEXT,
    IN p_indicaciones TEXT,
    IN p_contraindicaciones TEXT,
    IN p_dosis_recomendada VARCHAR(100),
    IN p_precio_base DECIMAL(10,2)
)
BEGIN
    DECLARE nuevo_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error al crear medicamento' AS error;
    END;
    
    START TRANSACTION;
    
    -- Insertar medicamento
    INSERT INTO medicamentos (
        nombre, 
        principio_activo, 
        id_categoria, 
        descripcion, 
        indicaciones, 
        contraindicaciones, 
        dosis_recomendada
    ) VALUES (
        p_nombre,
        p_principio_activo,
        p_id_categoria,
        p_descripcion,
        p_indicaciones,
        p_contraindicaciones,
        p_dosis_recomendada
    );
    
    SET nuevo_id = LAST_INSERT_ID();
    
    -- El trigger automáticamente creará los precios, pero actualizamos con el precio proporcionado
    IF p_precio_base IS NOT NULL AND p_precio_base > 0 THEN
        UPDATE precios_proveedor 
        SET precio_base = p_precio_base
        WHERE id_medicamento = nuevo_id;
    END IF;
    
    COMMIT;
    
    SELECT 
        nuevo_id AS id_medicamento_creado,
        'Medicamento creado exitosamente con precios en todos los proveedores' AS mensaje;
END$$
DELIMITER ;

-- Ejecutar sincronización inicial
CALL sincronizar_precios_medicamentos();

-- Verificación
SELECT 
    'Medicamentos sin precios' AS verificacion,
    COUNT(*) AS cantidad
FROM medicamentos m
WHERE NOT EXISTS (
    SELECT 1 FROM precios_proveedor pp 
    WHERE pp.id_medicamento = m.id_medicamento 
    AND pp.estado = 'Activo'
);
