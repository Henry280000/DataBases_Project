from mysql.connector import Error
from datetime import datetime, timedelta
import json


class MySQLModels:    
    def __init__(self, connection):
        self.connection = connection
    
    def _execute_query(self, query, params=None, fetch=True, fetchone=False):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchone() if fetchone else cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
        
        except Error as e:
            print(f"Error ejecutando query: {e}")
            return None if fetch else False
    
    # usuarios
    def get_user_by_username(self, username):
        query = "SELECT * FROM usuarios WHERE username = %s"
        return self._execute_query(query, (username,), fetchone=True)
    
    def update_last_access(self, user_id):
        query = "UPDATE usuarios SET ultimo_acceso = NOW() WHERE id_usuario = %s"
        return self._execute_query(query, (user_id,), fetch=False)
    
    def get_all_usuarios(self):
        query = """
            SELECT id_usuario AS id, nombre_completo AS nombre, username, email, 
                   rol, telefono, activo, fecha_creacion, ultimo_acceso
            FROM usuarios
            ORDER BY fecha_creacion DESC
        """
        return self._execute_query(query)
    
    # INVENTARIO
    def get_inventario_actual(self):
        query = """
            SELECT 
                codigo_lote,
                medicamento AS nombre_medicamento,
                categoria,
                cantidad_actual AS cantidad_disponible,
                precio_unitario,
                fecha_caducidad,
                dias_hasta_caducidad AS dias_para_caducar,
                estado
            FROM v_inventario_actual 
            ORDER BY medicamento
        """
        return self._execute_query(query)
    
    def get_all_medicamentos(self):
        query = """
            SELECT m.id_medicamento AS id, m.nombre, m.principio_activo, 
                   c.nombre AS categoria_nombre,
                   COALESCE(AVG(l.precio_unitario), 0) AS precio,
                   COALESCE(SUM(l.cantidad_actual), 0) AS stock_total
            FROM medicamentos m
            JOIN categorias c ON m.id_categoria = c.id_categoria
            LEFT JOIN lotes l ON m.id_medicamento = l.id_medicamento 
                AND l.estado = 'Disponible'
            GROUP BY m.id_medicamento
            ORDER BY m.nombre
        """
        return self._execute_query(query)
    
    def get_medicamento_by_id(self, medicamento_id):
        query = """
            SELECT m.*, c.nombre AS categoria_nombre,
                   COALESCE(AVG(l.precio_unitario), 0) AS precio
            FROM medicamentos m
            JOIN categorias c ON m.id_categoria = c.id_categoria
            LEFT JOIN lotes l ON m.id_medicamento = l.id_medicamento 
                AND l.estado = 'Disponible'
            WHERE m.id_medicamento = %s
            GROUP BY m.id_medicamento
        """
        return self._execute_query(query, (medicamento_id,), fetchone=True)
    
    def get_all_lotes(self):
        query = """
            SELECT l.*, m.nombre AS medicamento_nombre
            FROM lotes l
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            ORDER BY l.fecha_caducidad
        """
        return self._execute_query(query)
    
    def get_lote_by_id(self, lote_id):
        query = """
            SELECT l.*, m.nombre AS medicamento_nombre, 
                   m.principio_activo, c.nombre AS categoria
            FROM lotes l
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            JOIN categorias c ON m.id_categoria = c.id_categoria
            WHERE l.id_lote = %s
        """
        return self._execute_query(query, (lote_id,), fetchone=True)
    
    def get_medicamentos_por_caducar(self):
        query = """
            SELECT 
                l.codigo_lote,
                m.nombre AS medicamento_nombre,
                l.cantidad_actual AS cantidad_disponible,
                l.fecha_caducidad,
                DATEDIFF(l.fecha_caducidad, CURDATE()) AS dias_restantes
            FROM lotes l
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            WHERE l.estado = 'Disponible'
              AND DATEDIFF(l.fecha_caducidad, CURDATE()) BETWEEN 0 AND 90
            ORDER BY dias_restantes ASC
            LIMIT 50
        """
        return self._execute_query(query)
    
    def get_lotes_caducados(self):
        query = """
            SELECT 
                l.id_lote,
                l.codigo_lote,
                m.nombre AS medicamento_nombre,
                l.cantidad_actual,
                l.fecha_caducidad,
                DATEDIFF(CURDATE(), l.fecha_caducidad) AS dias_caducado
            FROM lotes l
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            WHERE l.fecha_caducidad < CURDATE()
              AND l.cantidad_actual > 0
            ORDER BY l.fecha_caducidad DESC
        """
        return self._execute_query(query)
    
    def eliminar_lote_caducado(self, lote_id):
        query = "UPDATE lotes SET cantidad_actual = 0, estado = 'Caducado' WHERE id_lote = %s"
        return self._execute_query(query, (lote_id,), fetch=False)
    
    def get_all_categorias(self):
        query = "SELECT * FROM categorias ORDER BY nombre"
        return self._execute_query(query)
    
    def sincronizar_precios_medicamentos(self):
        # Sincroniza precios de proveedores para medicamentos sin precios configurados
        try:
            cursor = self.connection.cursor()
            query = """
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
                    50.00,
                    30,
                    5.00,
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
                )
            """
            cursor.execute(query)
            registros = cursor.rowcount
            self.connection.commit()
            cursor.close()
            return {'success': True, 'registros_creados': registros}
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {'success': False, 'error': str(e)}
    
    def crear_medicamento(self, nombre, principio_activo, id_categoria, descripcion=None, indicaciones=None, contraindicaciones=None, dosis_recomendada=None):
        # Crea un medicamento y automáticamente genera precios para todos los proveedores
        try:
            cursor = self.connection.cursor()
            
            # Insertar medicamento
            query = """
                INSERT INTO medicamentos 
                (nombre, principio_activo, id_categoria, descripcion, indicaciones, contraindicaciones, dosis_recomendada)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (nombre, principio_activo, id_categoria, descripcion, indicaciones, contraindicaciones, dosis_recomendada)
            cursor.execute(query, params)
            medicamento_id = cursor.lastrowid
            
            # Crear precios automáticamente para todos los proveedores activos
            query_precios = """
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
                    %s,
                    50.00,
                    30,
                    5.00,
                    CURDATE(),
                    'Activo'
                FROM proveedores p
                WHERE p.activo = TRUE
            """
            cursor.execute(query_precios, (medicamento_id,))
            
            self.connection.commit()
            cursor.close()
            return medicamento_id
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"Error creando medicamento: {e}")
            return None
    
    # ventas
    def get_all_ventas(self):
        query = """
            SELECT v.*, c.nombre AS cliente_nombre, u.nombre_completo AS vendedor
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
            LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            ORDER BY v.fecha_venta DESC
            LIMIT 1000
        """
        return self._execute_query(query)
    
    def get_venta_by_id(self, venta_id):
        query_venta = """
            SELECT v.*, c.nombre AS cliente_nombre, u.nombre_completo AS vendedor
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
            LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            WHERE v.id_venta = %s
        """
        query_detalles = """
            SELECT dv.*, l.codigo_lote, m.nombre AS medicamento_nombre
            FROM detalles_venta dv
            JOIN lotes l ON dv.id_lote = l.id_lote
            JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            WHERE dv.id_venta = %s
        """
        
        venta = self._execute_query(query_venta, (venta_id,), fetchone=True)
        if venta:
            venta['detalles'] = self._execute_query(query_detalles, (venta_id,))
        
        return venta
    
    def registrar_venta(self, id_cliente, id_usuario, metodo_pago, detalles):
        try:
            cursor = self.connection.cursor()
            
            # Llamar al procedimiento almacenado
            args = [id_cliente, id_usuario, metodo_pago, detalles, None, None]
            result = cursor.callproc('sp_registrar_venta', args)
            
            # Obtener resultados (OUT parameters están en posiciones 4 y 5)
            id_venta = result[4]
            mensaje = result[5]
            
            cursor.close()
            self.connection.commit()
            
            return {
                'success': id_venta is not None,
                'id_venta': id_venta,
                'mensaje': mensaje
            }
        
        except Error as e:
            return {'success': False, 'mensaje': str(e)}
    
    def get_all_clientes(self):
        query = "SELECT * FROM clientes ORDER BY nombre"
        return self._execute_query(query)
    
    # ÓRDENES DE COMPRA
    
    def get_all_ordenes_compra(self):
        query = """
            SELECT oc.*, p.nombre AS proveedor_nombre
            FROM ordenes_compra oc
            JOIN proveedores p ON oc.id_proveedor = p.id_proveedor
            ORDER BY oc.fecha_orden DESC
        """
        return self._execute_query(query)
    
    def crear_orden_compra(self, data):
        try:
            cursor = self.connection.cursor()
            self.connection.start_transaction()
            
            # Insertar orden de compra
            query_orden = """
                INSERT INTO ordenes_compra 
                (numero_orden, id_proveedor, fecha_orden, fecha_entrega_esperada, 
                 estado, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            params_orden = (
                data['numero_orden'],
                data['id_proveedor'],
                data['fecha_orden'],
                data.get('fecha_entrega_esperada'),
                data.get('estado', 'Pendiente'),
                data.get('observaciones')
            )
            
            cursor.execute(query_orden, params_orden)
            orden_id = cursor.lastrowid
            
            # Insertar detalles
            query_detalle = """
                INSERT INTO detalles_orden_compra 
                (id_orden_compra, id_medicamento, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """
            
            total = 0
            for detalle in data.get('detalles', []):
                params_detalle = (
                    orden_id,
                    detalle['id_medicamento'],
                    detalle['cantidad'],
                    detalle['precio_unitario']
                )
                cursor.execute(query_detalle, params_detalle)
                total += detalle['cantidad'] * detalle['precio_unitario']
            
            # Actualizar total
            cursor.execute(
                "UPDATE ordenes_compra SET total = %s WHERE id_orden_compra = %s",
                (total, orden_id)
            )
            
            self.connection.commit()
            cursor.close()
            
            return {'success': True, 'id_orden_compra': orden_id}
        
        except Error as e:
            self.connection.rollback()
            return {'success': False, 'mensaje': str(e)}
    
    def get_all_proveedores(self):
        query = """
            SELECT id_proveedor AS id, nombre, rfc, telefono, email, contacto_principal, activo
            FROM proveedores 
            WHERE activo = TRUE 
            ORDER BY nombre
        """
        return self._execute_query(query)
    
    def get_precio_proveedor(self, id_proveedor, id_medicamento, cantidad):
        query = """
            SELECT 
                pp.precio_base,
                pp.cantidad_minima_descuento,
                pp.porcentaje_descuento,
                CASE 
                    WHEN %s >= pp.cantidad_minima_descuento 
                    THEN pp.precio_base * (1 - pp.porcentaje_descuento / 100)
                    ELSE pp.precio_base
                END AS precio_final,
                CASE 
                    WHEN %s >= pp.cantidad_minima_descuento 
                    THEN CONCAT('Descuento aplicado: ', pp.porcentaje_descuento, '%%')
                    ELSE CONCAT('Cantidad mínima para descuento: ', pp.cantidad_minima_descuento)
                END AS mensaje_descuento,
                m.nombre AS medicamento_nombre,
                p.nombre AS proveedor_nombre
            FROM precios_proveedor pp
            JOIN medicamentos m ON pp.id_medicamento = m.id_medicamento
            JOIN proveedores p ON pp.id_proveedor = p.id_proveedor
            WHERE pp.id_proveedor = %s 
              AND pp.id_medicamento = %s
              AND pp.estado = 'Activo'
              AND pp.fecha_vigencia_inicio <= CURDATE()
              AND (pp.fecha_vigencia_fin IS NULL OR pp.fecha_vigencia_fin >= CURDATE())
            LIMIT 1
        """
        return self._execute_query(query, (cantidad, cantidad, id_proveedor, id_medicamento))
    
    def get_medicamentos_por_proveedor(self, id_proveedor):
        query = """
            SELECT 
                m.id_medicamento,
                m.nombre,
                m.principio_activo,
                pp.precio_base,
                pp.cantidad_minima_descuento,
                pp.porcentaje_descuento,
                CONCAT('$', FORMAT(pp.precio_base, 2), ' - Desc. ', 
                       pp.porcentaje_descuento, '%% desde ', 
                       pp.cantidad_minima_descuento, ' unidades') AS info_precio
            FROM precios_proveedor pp
            JOIN medicamentos m ON pp.id_medicamento = m.id_medicamento
            WHERE pp.id_proveedor = %s
              AND pp.estado = 'Activo'
              AND pp.fecha_vigencia_inicio <= CURDATE()
              AND (pp.fecha_vigencia_fin IS NULL OR pp.fecha_vigencia_fin >= CURDATE())
            ORDER BY m.nombre
        """
        return self._execute_query(query, (id_proveedor,))
    
    def get_estadisticas_ventas(self):
        query = """
            SELECT 
                COUNT(*) AS total_ventas,
                SUM(total) AS monto_total,
                AVG(total) AS promedio_venta,
                MIN(fecha_venta) AS primera_venta,
                MAX(fecha_venta) AS ultima_venta
            FROM ventas
            WHERE estado = 'Completada'
        """
        return self._execute_query(query, fetchone=True)
    
    def get_estadisticas_inventario(self):
        query = """
            SELECT 
                COUNT(DISTINCT id_medicamento) AS total_medicamentos,
                COUNT(*) AS total_lotes,
                SUM(cantidad_actual) AS unidades_total,
                SUM(cantidad_actual * precio_unitario) AS valor_total,
                COUNT(CASE WHEN DATEDIFF(fecha_caducidad, CURDATE()) BETWEEN 0 AND 90 THEN 1 END) AS lotes_proximos_caducar
            FROM lotes
            WHERE estado = 'Disponible'
        """
        return self._execute_query(query, fetchone=True)
    
    def get_auditoria(self, limit=100):
        query = """
            SELECT a.*, u.nombre_completo AS usuario_nombre
            FROM auditoria_transacciones a
            LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario
            ORDER BY a.fecha_operacion DESC
            LIMIT %s
        """
        return self._execute_query(query, (limit,))
        
    def registrar_venta_simple(self, medicamento_id, cantidad, precio_unitario, total, 
                               cliente_nombre, metodo_pago, vendedor_id, observaciones=''):
        try:
            cursor = self.connection.cursor()
            
            # Buscar o crear cliente general
            cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = %s LIMIT 1", (cliente_nombre,))
            cliente_row = cursor.fetchone()
            
            if not cliente_row:
                # Crear cliente temporal
                cursor.execute("""
                    INSERT INTO clientes (nombre, email, telefono) 
                    VALUES (%s, 'general@pharmaflow.com', 'N/A')
                """, (cliente_nombre,))
                id_cliente = cursor.lastrowid
            else:
                id_cliente = cliente_row[0]
            
            # Buscar lote disponible del medicamento con suficiente stock
            cursor.execute("""
                SELECT id_lote, precio_unitario 
                FROM lotes 
                WHERE id_medicamento = %s 
                  AND estado = 'Disponible' 
                  AND cantidad_actual >= %s
                ORDER BY fecha_caducidad ASC
                LIMIT 1
            """, (medicamento_id, cantidad))
            
            lote_row = cursor.fetchone()
            if not lote_row:
                cursor.close()
                return {'success': False, 'mensaje': 'No hay stock suficiente del medicamento'}
            
            id_lote = lote_row[0]
            precio_lote = lote_row[1]
            
            # Generar número de venta
            numero_venta = f"VNT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Insertar venta
            query_venta = """
                INSERT INTO ventas (numero_venta, id_cliente, fecha_venta, 
                                   total, metodo_pago, estado, observaciones, id_usuario)
                VALUES (%s, %s, NOW(), %s, %s, 'Completada', %s, %s)
            """
            cursor.execute(query_venta, (numero_venta, id_cliente, total, metodo_pago, 
                                        observaciones, vendedor_id))
            venta_id = cursor.lastrowid
            
            # Insertar detalle de venta (usa id_lote, no id_medicamento)
            query_detalle = """
                INSERT INTO detalles_venta (id_venta, id_lote, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_detalle, (venta_id, id_lote, cantidad, precio_unitario))
            
            # Actualizar stock del lote
            cursor.execute("""
                UPDATE lotes 
                SET cantidad_actual = cantidad_actual - %s
                WHERE id_lote = %s
            """, (cantidad, id_lote))
            
            self.connection.commit()
            cursor.close()
            return {'success': True, 'id_venta': venta_id, 'mensaje': 'Venta registrada exitosamente'}
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {'success': False, 'mensaje': f'Error al registrar venta: {str(e)}'}
    
    def get_ventas_recientes(self, limit=50):
        query = """
            SELECT v.id_venta AS id, v.numero_venta, v.fecha_venta, 
                   v.total, v.metodo_pago, v.estado, v.observaciones,
                   c.nombre AS cliente_nombre,
                   GROUP_CONCAT(m.nombre SEPARATOR ', ') AS medicamento_nombre,
                   SUM(dv.cantidad) AS cantidad,
                   u.nombre_completo AS vendedor_nombre
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
            LEFT JOIN detalles_venta dv ON v.id_venta = dv.id_venta
            LEFT JOIN lotes l ON dv.id_lote = l.id_lote
            LEFT JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
            LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            GROUP BY v.id_venta
            ORDER BY v.fecha_venta DESC
            LIMIT %s
        """
        return self._execute_query(query, (limit,))
    
    def get_ventas_stats(self):
        query = """
            SELECT 
                COUNT(CASE WHEN DATE(fecha_venta) = CURDATE() THEN 1 END) AS ventas_hoy,
                COALESCE(SUM(CASE WHEN DATE(fecha_venta) = CURDATE() THEN total END), 0) AS ingresos_hoy,
                COUNT(CASE WHEN MONTH(fecha_venta) = MONTH(CURDATE()) AND YEAR(fecha_venta) = YEAR(CURDATE()) THEN 1 END) AS ventas_mes,
                COALESCE(SUM(CASE WHEN MONTH(fecha_venta) = MONTH(CURDATE()) AND YEAR(fecha_venta) = YEAR(CURDATE()) THEN total END), 0) AS ingresos_mes
            FROM ventas
        """
        return self._execute_query(query, fetchone=True)
    
    # funciones de ordenes de compra
    
    def registrar_orden_compra(self, proveedor_id, medicamento_id, cantidad, 
                                precio_unitario, total, observaciones=''):
        try:
            cursor = self.connection.cursor()
            
            # Generar número de orden
            numero_orden = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Insertar orden de compra
            query_orden = """
                INSERT INTO ordenes_compra (numero_orden, id_proveedor, fecha_orden, 
                                           estado, total, observaciones)
                VALUES (%s, %s, NOW(), 'Pendiente', %s, %s)
            """
            cursor.execute(query_orden, (numero_orden, proveedor_id, total, observaciones))
            orden_id = cursor.lastrowid
            
            # Insertar detalle de la orden
            query_detalle = """
                INSERT INTO detalles_orden_compra (id_orden_compra, id_medicamento, 
                                                  cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_detalle, (orden_id, medicamento_id, cantidad, precio_unitario))
            
            self.connection.commit()
            cursor.close()
            return {'success': True, 'id_orden': orden_id, 'mensaje': 'Orden creada exitosamente'}
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {'success': False, 'mensaje': f'Error al crear orden: {str(e)}'}
    
    def update_orden_estado(self, orden_id, nuevo_estado):
        try:
            query_update = """
                UPDATE ordenes_compra 
                SET estado = %s 
                WHERE id_orden_compra = %s
            """
            self._execute_query(query_update, (nuevo_estado, orden_id), fetch=False)
            
            if nuevo_estado == 'Recibida':
                query_detalles = """
                    SELECT doc.id_medicamento, doc.cantidad, doc.precio_unitario
                    FROM detalles_orden_compra doc
                    WHERE doc.id_orden_compra = %s
                """
                detalles = self._execute_query(query_detalles, (orden_id,))
                
                for detalle in detalles:
                    codigo_lote = f"LOTE-{datetime.now().strftime('%Y%m%d%H%M%S')}-{detalle['id_medicamento']}"
                    fecha_caducidad = datetime.now() + timedelta(days=730)
                    
                    query_lote = """
                        INSERT INTO lotes (codigo_lote, id_medicamento, cantidad_inicial, cantidad_actual, 
                                         precio_unitario, fecha_fabricacion, fecha_caducidad, estado)
                        VALUES (%s, %s, %s, %s, %s, NOW(), %s, 'Disponible')
                    """
                    self._execute_query(query_lote, (
                        codigo_lote,
                        detalle['id_medicamento'],
                        detalle['cantidad'],
                        detalle['cantidad'],
                        detalle['precio_unitario'],
                        fecha_caducidad.strftime('%Y-%m-%d')
                    ), fetch=False)
            
            if self.connection:
                self.connection.commit()
            return {'success': True, 'mensaje': f'Estado actualizado a {nuevo_estado}'}
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {'success': False, 'mensaje': f'Error al actualizar estado: {str(e)}'}
    
    def get_ordenes_recientes(self, limit=50):
        query = """
            SELECT oc.id_orden_compra AS id, oc.numero_orden, oc.fecha_orden, 
                   oc.estado, oc.total, oc.observaciones,
                   p.nombre AS proveedor_nombre,
                   GROUP_CONCAT(m.nombre SEPARATOR ', ') AS medicamento_nombre,
                   SUM(doc.cantidad) AS cantidad,
                   AVG(doc.precio_unitario) AS precio_unitario
            FROM ordenes_compra oc
            JOIN proveedores p ON oc.id_proveedor = p.id_proveedor
            LEFT JOIN detalles_orden_compra doc ON oc.id_orden_compra = doc.id_orden_compra
            LEFT JOIN medicamentos m ON doc.id_medicamento = m.id_medicamento
            GROUP BY oc.id_orden_compra
            ORDER BY oc.fecha_orden DESC
            LIMIT %s
        """
        return self._execute_query(query, (limit,))
    
    def get_ordenes_stats(self):
        query = """
            SELECT 
                COUNT(CASE WHEN estado = 'Pendiente' THEN 1 END) AS ordenes_pendientes,
                COUNT(CASE WHEN MONTH(fecha_orden) = MONTH(CURDATE()) AND YEAR(fecha_orden) = YEAR(CURDATE()) THEN 1 END) AS ordenes_mes,
                COALESCE(SUM(CASE WHEN MONTH(fecha_orden) = MONTH(CURDATE()) AND YEAR(fecha_orden) = YEAR(CURDATE()) THEN total END), 0) AS total_mes,
                COUNT(DISTINCT id_proveedor) AS proveedores_activos
            FROM ordenes_compra
        """
        return self._execute_query(query, fetchone=True)
    
    # FUNCIONES DE USUARIO
    
    def registrar_usuario(self, nombre, email, username, password_hash, rol, telefono=None):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO usuarios (nombre_completo, email, username, password_hash, 
                                     rol, telefono, activo, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, 1, NOW())
            """
            cursor.execute(query, (nombre, email, username, password_hash, rol, telefono))
            self.connection.commit()
            usuario_id = cursor.lastrowid
            cursor.close()
            return {'success': True, 'id_usuario': usuario_id, 'mensaje': 'Usuario creado exitosamente'}
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {'success': False, 'mensaje': f'Error al crear usuario: {str(e)}'}
    
    def get_usuarios_stats(self):
        query = """
            SELECT 
                COUNT(*) AS total_usuarios,
                COUNT(CASE WHEN rol = 'Gerente' THEN 1 END) AS total_gerentes,
                COUNT(CASE WHEN rol = 'Farmacéutico' THEN 1 END) AS total_farmaceuticos,
                COUNT(CASE WHEN rol = 'Investigador' THEN 1 END) AS total_investigadores
            FROM usuarios
            WHERE activo = 1
        """
        return self._execute_query(query, fetchone=True)
