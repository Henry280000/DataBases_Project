
-- Crear la base de datos
DROP DATABASE IF EXISTS pharmaflow_relational;
CREATE DATABASE pharmaflow_relational CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pharmaflow_relational;

-- Tabla de Categorías de Medicamentos
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB;

-- Tabla de Medicamentos
CREATE TABLE medicamentos (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    principio_activo VARCHAR(200) NOT NULL,
    id_categoria INT NOT NULL,
    descripcion TEXT,
    indicaciones TEXT,
    contraindicaciones TEXT,
    dosis_recomendada VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE RESTRICT,
    INDEX idx_nombre (nombre),
    INDEX idx_principio_activo (principio_activo),
    INDEX idx_categoria (id_categoria)
) ENGINE=InnoDB;

-- Tabla de Lotes de Inventario (Control de Stock)
CREATE TABLE lotes (
    id_lote INT AUTO_INCREMENT PRIMARY KEY,
    codigo_lote VARCHAR(50) NOT NULL UNIQUE,
    id_medicamento INT NOT NULL,
    cantidad_inicial INT NOT NULL CHECK (cantidad_inicial >= 0),
    cantidad_actual INT NOT NULL CHECK (cantidad_actual >= 0),
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario > 0),
    fecha_fabricacion DATE NOT NULL,
    fecha_caducidad DATE NOT NULL,
    ubicacion_almacen VARCHAR(50),
    estado ENUM('Disponible', 'Reservado', 'Caducado', 'Agotado') DEFAULT 'Disponible',
    version INT DEFAULT 0, -- Para control de concurrencia optimista
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) ON DELETE RESTRICT,
    INDEX idx_codigo_lote (codigo_lote),
    INDEX idx_medicamento (id_medicamento),
    INDEX idx_fecha_caducidad (fecha_caducidad),
    INDEX idx_estado (estado),
    CHECK (fecha_caducidad > fecha_fabricacion),
    CHECK (cantidad_actual <= cantidad_inicial)
) ENGINE=InnoDB;

-- Tabla de Proveedores
CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    rfc VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    contacto_principal VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_activo (activo)
) ENGINE=InnoDB;

-- Tabla de Órdenes de Compra
CREATE TABLE ordenes_compra (
    id_orden_compra INT AUTO_INCREMENT PRIMARY KEY,
    numero_orden VARCHAR(50) NOT NULL UNIQUE,
    id_proveedor INT NOT NULL,
    fecha_orden DATE NOT NULL,
    fecha_entrega_esperada DATE,
    fecha_entrega_real DATE,
    estado ENUM('Pendiente', 'Aprobada', 'Recibida', 'Cancelada') DEFAULT 'Pendiente',
    total DECIMAL(12, 2) DEFAULT 0,
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE RESTRICT,
    INDEX idx_numero_orden (numero_orden),
    INDEX idx_proveedor (id_proveedor),
    INDEX idx_estado (estado),
    INDEX idx_fecha_orden (fecha_orden)
) ENGINE=InnoDB;

-- Tabla de Detalles de Órdenes de Compra
CREATE TABLE detalles_orden_compra (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_orden_compra INT NOT NULL,
    id_medicamento INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario > 0),
    subtotal DECIMAL(12, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) ON DELETE RESTRICT,
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_medicamento (id_medicamento)
) ENGINE=InnoDB;

-- Tabla de Clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    tipo ENUM('Persona', 'Farmacia', 'Hospital', 'Clínica') NOT NULL,
    rfc VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_tipo (tipo)
) ENGINE=InnoDB;

-- Tabla de Ventas
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    numero_venta VARCHAR(50) NOT NULL UNIQUE,
    id_cliente INT,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(12, 2) DEFAULT 0,
    metodo_pago ENUM('Efectivo', 'Tarjeta', 'Transferencia', 'Crédito') DEFAULT 'Efectivo',
    estado ENUM('Completada', 'Cancelada', 'Pendiente') DEFAULT 'Completada',
    observaciones TEXT,
    id_usuario INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE SET NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    INDEX idx_numero_venta (numero_venta),
    INDEX idx_cliente (id_cliente),
    INDEX idx_fecha_venta (fecha_venta),
    INDEX idx_usuario (id_usuario)
) ENGINE=InnoDB;

-- Tabla de Detalles de Ventas
CREATE TABLE detalles_venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_lote INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario > 0),
    subtotal DECIMAL(12, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_lote) REFERENCES lotes(id_lote) ON DELETE RESTRICT,
    INDEX idx_venta (id_venta),
    INDEX idx_lote (id_lote)
) ENGINE=InnoDB;

-- Tabla de Usuarios del Sistema
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    rol ENUM('Gerente', 'Farmacéutico', 'Investigador') NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_rol (rol),
    INDEX idx_activo (activo)
) ENGINE=InnoDB;

-- Tabla de Auditoría de Transacciones
CREATE TABLE auditoria_transacciones (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    tabla_afectada VARCHAR(50) NOT NULL,
    id_registro INT NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    id_usuario INT,
    fecha_operacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores JSON,
    datos_nuevos JSON,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    INDEX idx_tabla (tabla_afectada),
    INDEX idx_fecha (fecha_operacion),
    INDEX idx_usuario (id_usuario)
) ENGINE=InnoDB;

-- Vista de Inventario Actual
CREATE VIEW v_inventario_actual AS
SELECT 
    l.id_lote,
    l.codigo_lote,
    m.nombre AS medicamento,
    m.principio_activo,
    c.nombre AS categoria,
    l.cantidad_actual,
    l.precio_unitario,
    l.fecha_caducidad,
    l.ubicacion_almacen,
    l.estado,
    DATEDIFF(l.fecha_caducidad, CURDATE()) AS dias_hasta_caducidad
FROM lotes l
JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
JOIN categorias c ON m.id_categoria = c.id_categoria
WHERE l.cantidad_actual > 0 AND l.estado = 'Disponible';

-- Vista de Medicamentos Próximos a Caducar
CREATE VIEW v_medicamentos_por_caducar AS
SELECT 
    l.codigo_lote,
    m.nombre AS medicamento,
    l.cantidad_actual,
    l.fecha_caducidad,
    DATEDIFF(l.fecha_caducidad, CURDATE()) AS dias_restantes
FROM lotes l
JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
WHERE l.fecha_caducidad <= DATE_ADD(CURDATE(), INTERVAL 90 DAY)
    AND l.cantidad_actual > 0
    AND l.estado = 'Disponible'
ORDER BY l.fecha_caducidad;

-- Vista de Estadísticas de Ventas
CREATE VIEW v_estadisticas_ventas AS
SELECT 
    DATE(v.fecha_venta) AS fecha,
    COUNT(*) AS total_ventas,
    SUM(v.total) AS monto_total,
    AVG(v.total) AS promedio_venta,
    u.nombre_completo AS vendedor
FROM ventas v
LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
WHERE v.estado = 'Completada'
GROUP BY DATE(v.fecha_venta), u.nombre_completo;

DELIMITER //

-- Procedimiento para Registrar una Venta 
CREATE PROCEDURE sp_registrar_venta(
    IN p_id_cliente INT,
    IN p_id_usuario INT,
    IN p_metodo_pago VARCHAR(20),
    IN p_detalles JSON,
    OUT p_id_venta INT,
    OUT p_mensaje VARCHAR(255)
)
BEGIN
    DECLARE v_lote_id INT;
    DECLARE v_cantidad INT;
    DECLARE v_precio DECIMAL(10,2);
    DECLARE v_cantidad_disponible INT;
    DECLARE v_version_actual INT;
    DECLARE v_numero_venta VARCHAR(50);
    DECLARE v_total DECIMAL(12,2) DEFAULT 0;
    DECLARE v_index INT DEFAULT 0;
    DECLARE v_detalle_count INT;
    DECLARE exit handler FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_mensaje = 'Error en la transacción. Venta cancelada.';
        SET p_id_venta = NULL;
    END;
    
    -- Iniciar transacción
    START TRANSACTION;
    
    -- Generar número de venta
    SET v_numero_venta = CONCAT('VNT-', DATE_FORMAT(NOW(), '%Y%m%d'), '-', LPAD((SELECT IFNULL(MAX(id_venta), 0) + 1 FROM ventas), 6, '0'));
    
    -- Crear la venta
    INSERT INTO ventas (numero_venta, id_cliente, id_usuario, metodo_pago, total)
    VALUES (v_numero_venta, p_id_cliente, p_id_usuario, p_metodo_pago, 0);
    
    SET p_id_venta = LAST_INSERT_ID();
    
    -- Obtener cantidad de detalles
    SET v_detalle_count = JSON_LENGTH(p_detalles);
    
    -- Procesar cada detalle
    WHILE v_index < v_detalle_count DO
        SET v_lote_id = JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[', v_index, '].id_lote')));
        SET v_cantidad = JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[', v_index, '].cantidad')));
        SET v_precio = JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[', v_index, '].precio')));
        
        -- Bloquear el lote para lectura (SELECT FOR UPDATE)
        SELECT cantidad_actual, version INTO v_cantidad_disponible, v_version_actual
        FROM lotes
        WHERE id_lote = v_lote_id
        FOR UPDATE;
        
        -- Verificar disponibilidad
        IF v_cantidad_disponible < v_cantidad THEN
            ROLLBACK;
            SET p_mensaje = CONCAT('Stock insuficiente para lote ID: ', v_lote_id);
            SET p_id_venta = NULL;
            LEAVE;
        END IF;
        
        -- Registrar detalle de venta
        INSERT INTO detalles_venta (id_venta, id_lote, cantidad, precio_unitario)
        VALUES (p_id_venta, v_lote_id, v_cantidad, v_precio);
        
        -- Actualizar inventario con control de concurrencia optimista
        UPDATE lotes
        SET cantidad_actual = cantidad_actual - v_cantidad,
            version = version + 1,
            estado = CASE 
                WHEN cantidad_actual - v_cantidad = 0 THEN 'Agotado'
                ELSE estado
            END
        WHERE id_lote = v_lote_id AND version = v_version_actual;
        
        -- Verificar que se actualizó (concurrencia optimista)
        IF ROW_COUNT() = 0 THEN
            ROLLBACK;
            SET p_mensaje = 'Conflicto de concurrencia. Intente nuevamente.';
            SET p_id_venta = NULL;
            LEAVE;
        END IF;
        
        SET v_total = v_total + (v_cantidad * v_precio);
        SET v_index = v_index + 1;
    END WHILE;
    
    -- Actualizar total de la venta
    IF p_id_venta IS NOT NULL THEN
        UPDATE ventas SET total = v_total WHERE id_venta = p_id_venta;
        COMMIT;
        SET p_mensaje = 'Venta registrada exitosamente';
    END IF;
END //

-- Procedimiento para actualizar estado de lotes caducados
CREATE PROCEDURE sp_actualizar_lotes_caducados()
BEGIN
    UPDATE lotes
    SET estado = 'Caducado'
    WHERE fecha_caducidad < CURDATE() AND estado != 'Caducado';
    
    SELECT ROW_COUNT() AS lotes_actualizados;
END //

-- Función para calcular valor total de inventario
CREATE FUNCTION fn_valor_inventario_total()
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(15,2);
    
    SELECT SUM(cantidad_actual * precio_unitario) INTO total
    FROM lotes
    WHERE estado = 'Disponible';
    
    RETURN IFNULL(total, 0);
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_lotes_after_update
AFTER UPDATE ON lotes
FOR EACH ROW
BEGIN
    IF OLD.cantidad_actual != NEW.cantidad_actual THEN
        INSERT INTO auditoria_transacciones (
            tabla_afectada, id_registro, tipo_operacion, datos_anteriores, datos_nuevos
        )
        VALUES (
            'lotes',
            NEW.id_lote,
            'UPDATE',
            JSON_OBJECT('cantidad_actual', OLD.cantidad_actual, 'version', OLD.version),
            JSON_OBJECT('cantidad_actual', NEW.cantidad_actual, 'version', NEW.version)
        );
    END IF;
END //

CREATE TRIGGER trg_ventas_after_insert
AFTER INSERT ON ventas
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_transacciones (
        tabla_afectada, id_registro, tipo_operacion, id_usuario, datos_nuevos
    )
    VALUES (
        'ventas',
        NEW.id_venta,
        'INSERT',
        NEW.id_usuario,
        JSON_OBJECT('numero_venta', NEW.numero_venta, 'total', NEW.total)
    );
END //

DELIMITER ;

-- Índice compuesto para búsquedas frecuentes de inventario
CREATE INDEX idx_lote_medicamento_estado ON lotes(id_medicamento, estado, fecha_caducidad);

-- Índice para optimizar reportes de ventas por fecha
CREATE INDEX idx_ventas_fecha_estado ON ventas(fecha_venta, estado);

-- Índice para búsquedas de órdenes de compra
CREATE INDEX idx_ordenes_fecha_estado ON ordenes_compra(fecha_orden, estado);
