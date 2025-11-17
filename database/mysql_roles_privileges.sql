USE pharmaflow_relational;

-- ROL 1: GERENTE
-- Acceso total a inventario y usuarios
-- Puede realizar todas las operaciones CRUD
CREATE USER IF NOT EXISTS 'gerente_user'@'localhost' IDENTIFIED BY 'Gerente2024!';

-- Privilegios completos sobre inventario
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.medicamentos TO 'gerente_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.categorias TO 'gerente_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.lotes TO 'gerente_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.proveedores TO 'gerente_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.clientes TO 'gerente_user'@'localhost';

-- Privilegios completos sobre transacciones
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.ventas TO 'gerente_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.detalles_venta TO 'gerente_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.ordenes_compra TO 'gerente_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON pharmaflow_relational.detalles_orden_compra TO 'gerente_user'@'localhost';

-- Privilegios sobre usuarios (gestión de personal)
GRANT SELECT, INSERT, UPDATE ON pharmaflow_relational.usuarios TO 'gerente_user'@'localhost';

-- Acceso a auditoría (solo lectura)
GRANT SELECT ON pharmaflow_relational.auditoria_transacciones TO 'gerente_user'@'localhost';

-- Acceso a vistas
GRANT SELECT ON pharmaflow_relational.v_inventario_actual TO 'gerente_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.v_medicamentos_por_caducar TO 'gerente_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.v_estadisticas_ventas TO 'gerente_user'@'localhost';

-- Acceso a procedimientos almacenados
GRANT EXECUTE ON PROCEDURE pharmaflow_relational.sp_registrar_venta TO 'gerente_user'@'localhost';
GRANT EXECUTE ON PROCEDURE pharmaflow_relational.sp_actualizar_lotes_caducados TO 'gerente_user'@'localhost';

-- Acceso a funciones
GRANT EXECUTE ON FUNCTION pharmaflow_relational.fn_valor_inventario_total TO 'gerente_user'@'localhost';

-- ROL 2: FARMACÉUTICO
-- Solo puede registrar ventas y modificar lotes
-- No puede eliminar registros ni acceder a usuarios
CREATE USER IF NOT EXISTS 'farmaceutico_user'@'localhost' IDENTIFIED BY 'Farmaceutico2024!';

-- Privilegios de lectura sobre medicamentos y categorías
GRANT SELECT ON pharmaflow_relational.medicamentos TO 'farmaceutico_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.categorias TO 'farmaceutico_user'@'localhost';

-- Privilegios sobre lotes (puede actualizar para ajustes de inventario)
GRANT SELECT, UPDATE ON pharmaflow_relational.lotes TO 'farmaceutico_user'@'localhost';

-- Privilegios sobre ventas (registrar ventas)
GRANT SELECT, INSERT ON pharmaflow_relational.ventas TO 'farmaceutico_user'@'localhost';
GRANT SELECT, INSERT ON pharmaflow_relational.detalles_venta TO 'farmaceutico_user'@'localhost';

-- Privilegios de lectura sobre clientes
GRANT SELECT ON pharmaflow_relational.clientes TO 'farmaceutico_user'@'localhost';

-- Privilegios limitados sobre proveedores (solo lectura)
GRANT SELECT ON pharmaflow_relational.proveedores TO 'farmaceutico_user'@'localhost';

-- Acceso a vistas
GRANT SELECT ON pharmaflow_relational.v_inventario_actual TO 'farmaceutico_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.v_medicamentos_por_caducar TO 'farmaceutico_user'@'localhost';

-- Acceso limitado a procedimientos (solo ventas)
GRANT EXECUTE ON PROCEDURE pharmaflow_relational.sp_registrar_venta TO 'farmaceutico_user'@'localhost';

-- ROL 3: INVESTIGADOR
-- Solo lectura en datos relacionales
-- Acceso completo a MongoDB (documentos NoSQL)

CREATE USER IF NOT EXISTS 'investigador_user'@'localhost' IDENTIFIED BY 'Investigador2024!';

-- Solo privilegios de lectura (SELECT)
GRANT SELECT ON pharmaflow_relational.medicamentos TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.categorias TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.lotes TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.proveedores TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.clientes TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.ventas TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.detalles_venta TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.ordenes_compra TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.detalles_orden_compra TO 'investigador_user'@'localhost';

-- Acceso a vistas (solo lectura)
GRANT SELECT ON pharmaflow_relational.v_inventario_actual TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.v_medicamentos_por_caducar TO 'investigador_user'@'localhost';
GRANT SELECT ON pharmaflow_relational.v_estadisticas_ventas TO 'investigador_user'@'localhost';

-- Acceso a funciones (solo lectura)
GRANT EXECUTE ON FUNCTION pharmaflow_relational.fn_valor_inventario_total TO 'investigador_user'@'localhost';

-- usuarios de aplicacion desde python
CREATE USER IF NOT EXISTS 'pharmaflow_app'@'localhost' IDENTIFIED BY 'AppPharma2024!';

-- Privilegios generales para operación de la aplicación
GRANT SELECT, INSERT, UPDATE ON pharmaflow_relational.* TO 'pharmaflow_app'@'localhost';

-- Permitir ejecución de procedimientos
GRANT EXECUTE ON pharmaflow_relational.* TO 'pharmaflow_app'@'localhost';
