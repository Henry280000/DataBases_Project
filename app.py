from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from functools import wraps
import os
from datetime import datetime, timedelta
import json
import bcrypt
import logging
import traceback

from models.database import DatabaseManager
from models.mysql_models import MySQLModels
from models.mongodb_models import MongoDBModels
from utils.security import hash_password, verify_password
from config.config import Config

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

CORS(app)

# Inicializar gestores de base de datos
db_manager = DatabaseManager()
mysql_models = MySQLModels(db_manager.mysql_conn)
mongodb_models = MongoDBModels(db_manager.mongo_db)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] not in roles:
                # Si es una petición API, devolver JSON
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'Permiso denegado'}), 403
                # Si es una página web, mostrar template de error
                return render_template('403.html'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # Obtener datos del formulario
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return render_template('login.html', error='Usuario y contraseña requeridos')
    
    # Buscar usuario
    user = mysql_models.get_user_by_username(username)
    
    if not user or not verify_password(password, user['password_hash']):
        return render_template('login.html', error='Credenciales inválidas')
    
    if not user['activo']:
        return render_template('login.html', error='Usuario inactivo')
    
    # Crear sesión
    session['user_id'] = user['id_usuario']
    session['username'] = user['username']
    session['user_role'] = user['rol']
    session['nombre_completo'] = user['nombre_completo']
    
    # Actualizar ultimo acceso
    mysql_models.update_last_access(user['id_usuario'])
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/user/info')
@login_required
def user_info():
    # Información del usuario actual
    return jsonify({
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'nombre_completo': session.get('nombre_completo'),
        'rol': session.get('user_role')
    })


@app.route('/dashboard')
@login_required
def dashboard():
    # Dashboard principal - Renderizado del lado del servidor
    try:
        # Obtener información del usuario
        usuario = {
            'nombre_completo': session.get('user_name', 'Usuario'),
            'rol': session.get('user_role', 'Desconocido')
        }
        
        # Obtener estadísticas del inventario
        try:
            stats_inventario = mysql_models.get_estadisticas_inventario()
            stats_ventas = mysql_models.get_estadisticas_ventas()
            
            logger.info(f"Stats inventario: {stats_inventario}")
            logger.info(f"Stats ventas: {stats_ventas}")
            
            estadisticas = {
                'valor_total': float(stats_inventario.get('valor_total', 0) or 0),
                'total_medicamentos': int(stats_inventario.get('total_medicamentos', 0) or 0),
                'ventas_mes': float(stats_ventas.get('monto_total', 0) or 0)
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            estadisticas = {
                'valor_total': 0,
                'total_medicamentos': 0,
                'ventas_mes': 0
            }
        
        # Obtener inventario (con opcion de busqueda)
        search_query = request.args.get('search', '')
        try:
            inventario = mysql_models.get_inventario_actual()
            
            # Filtrar por búsqueda si hay un término
            if search_query:
                inventario = [
                    item for item in inventario 
                    if search_query.lower() in item.get('nombre_medicamento', '').lower()
                    or search_query.lower() in item.get('codigo_lote', '').lower()
                ]
        except Exception as e:
            print(f"Error obteniendo inventario: {e}")
            inventario = []
        
        # Obtener medicamentos próximos a caducar
        try:
            medicamentos_caducar = mysql_models.get_medicamentos_por_caducar()
        except Exception as e:
            print(f"Error obteniendo medicamentos por caducar: {e}")
            medicamentos_caducar = []
        
        return render_template(
            'dashboard.html',
            usuario=usuario,
            estadisticas=estadisticas,
            inventario=inventario,
            medicamentos_caducar=medicamentos_caducar,
            request=request  # Para acceder a request.args en el template
        )
        
    except Exception as e:
        print(f"Error general en dashboard: {e}")
        return render_template('dashboard.html', 
                             usuario={'nombre_completo': 'Usuario', 'rol': 'Desconocido'},
                             estadisticas={'valor_total': 0, 'total_medicamentos': 0, 'lotes_por_caducar': 0, 'ventas_mes': 0},
                             inventario=[],
                             medicamentos_caducar=[])

@app.route('/api/inventario')
@login_required
def get_inventario():
    # Obtener inventario actual
    inventario = mysql_models.get_inventario_actual()
    return jsonify(inventario)

@app.route('/api/medicamentos')
@login_required
def get_medicamentos():
    # Obtener lista de medicamentos
    medicamentos = mysql_models.get_all_medicamentos()
    return jsonify(medicamentos)

@app.route('/api/medicamento/<int:id>')
@login_required
def get_medicamento(id):
    # Obtener detalle de un medicamento
    medicamento = mysql_models.get_medicamento_by_id(id)
    if not medicamento:
        return jsonify({'error': 'Medicamento no encontrado'}), 404
    return jsonify(medicamento)

@app.route('/api/lotes')
@login_required
def get_lotes():
    # Obtener lotes de inventario
    lotes = mysql_models.get_all_lotes()
    return jsonify(lotes)

@app.route('/api/lotes/caducar')
@login_required
def get_lotes_por_caducar():
    # Obtener medicamentos próximos a caducar
    lotes = mysql_models.get_medicamentos_por_caducar()
    return jsonify(lotes)

@app.route('/api/lote/<int:id>')
@login_required
def get_lote(id):
    # Obtener detalle de un lote
    lote = mysql_models.get_lote_by_id(id)
    if not lote:
        return jsonify({'error': 'Lote no encontrado'}), 404
    return jsonify(lote)


@app.route('/ventas', methods=['GET', 'POST'])
@login_required
@role_required('Gerente', 'Farmacéutico')
def ventas_page():
    # Página de ventas
    if request.method == 'POST':
        # Procesar nueva venta
        try:
            # Validar campos requeridos
            medicamento_id = request.form.get('medicamento_id')
            cantidad = request.form.get('cantidad')
            metodo_pago = request.form.get('metodo_pago')
            
            if not medicamento_id or not cantidad or not metodo_pago:
                raise ValueError("Todos los campos son requeridos")
            
            medicamento_id = int(medicamento_id)
            cantidad = int(cantidad)
            cliente_nombre = request.form.get('cliente_nombre') or 'Cliente General'
            observaciones = request.form.get('observaciones') or ''
            
            # Obtener precio del medicamento
            medicamento = mysql_models.get_medicamento_by_id(medicamento_id)
            if not medicamento:
                return render_template('ventas.html', mensaje='Medicamento no encontrado', mensaje_tipo='error')
            
            precio_unitario = medicamento['precio']
            total = precio_unitario * cantidad
            
            # Insertar venta
            result = mysql_models.registrar_venta_simple(
                medicamento_id=int(medicamento_id),
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                total=total,
                cliente_nombre=cliente_nombre,
                metodo_pago=metodo_pago,
                vendedor_id=session['user_id'],
                observaciones=observaciones
            )
            
            if result['success']:
                return redirect(url_for('ventas_page'))
            else:
                return render_template('ventas.html', mensaje=result['mensaje'], mensaje_tipo='error')
                
        except Exception as e:
            print(f"Error al registrar venta: {e}")
            return render_template('ventas.html', mensaje=f'Error: {str(e)}', mensaje_tipo='error')
    
    # Get - Mostrar página
    try:
        # Obtener estadísticas
        stats = mysql_models.get_ventas_stats()
        
        # Obtener medicamentos para el select
        medicamentos = mysql_models.get_all_medicamentos()
        
        # Obtener ventas recientes
        ventas = mysql_models.get_ventas_recientes()
        
        return render_template('ventas.html',
                             ventas=ventas,
                             medicamentos=medicamentos,
                             ventas_hoy=stats.get('ventas_hoy', 0),
                             total_hoy=stats.get('ingresos_hoy', 0),
                             ventas_mes=stats.get('ventas_mes', 0),
                             total_mes=stats.get('ingresos_mes', 0))
    except Exception as e:
        print(f"Error al cargar ventas: {e}")
        return render_template('ventas.html', ventas=[], medicamentos=[])

@app.route('/api/venta/<int:id>')
@login_required
def get_venta(id):
    # Obtener detalle de una venta
    venta = mysql_models.get_venta_by_id(id)
    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404
    return jsonify(venta)

@app.route('/api/clientes')
@login_required
def get_clientes():
    clientes = mysql_models.get_all_clientes()
    return jsonify(clientes)

@app.route('/api/medicamentos-proveedor/<int:id_proveedor>')
@login_required
def get_medicamentos_proveedor(id_proveedor):
    # Obtener medicamentos de un proveedor con precios (sincroniza automáticamente si faltan)
    # Sincronizar precios antes de consultar
    mysql_models.sincronizar_precios_medicamentos()
    medicamentos = mysql_models.get_medicamentos_por_proveedor(id_proveedor)
    return jsonify(medicamentos)

@app.route('/api/precio-proveedor')
@login_required
def get_precio_proveedor():
    # Calcular precio con descuento por cantidad
    id_proveedor = request.args.get('proveedor', type=int)
    id_medicamento = request.args.get('medicamento', type=int)
    cantidad = request.args.get('cantidad', type=int)
    
    if not all([id_proveedor, id_medicamento, cantidad]):
        return jsonify({'error': 'Parámetros incompletos'}), 400
    
    precio = mysql_models.get_precio_proveedor(id_proveedor, id_medicamento, cantidad)
    if not precio:
        return jsonify({'error': 'No hay precio configurado para esta combinación'}), 404
    
    return jsonify(precio[0] if precio else {})


@app.route('/ordenes-compra', methods=['GET', 'POST'])
@login_required
@role_required('Gerente')
def ordenes_compra_page():
    # Página de órdenes de compra con precios dinámicos por proveedor
    if request.method == 'POST':
        # Procesar nueva orden
        try:
            logger.info(f"Procesando nueva orden de compra. Form data: {request.form}")
            
            # Validar campos requeridos (observaciones es opcional)
            proveedor_id = request.form.get('proveedor_id', '').strip()
            medicamento_id = request.form.get('medicamento_id', '').strip()
            cantidad = request.form.get('cantidad', '').strip()
            precio_unitario = request.form.get('precio_unitario', '').strip()
            
            # Validar que los campos requeridos no estén vacíos
            errores = []
            if not proveedor_id:
                errores.append("Debe seleccionar un proveedor")
            if not medicamento_id:
                errores.append("Debe seleccionar un medicamento")
            if not cantidad:
                errores.append("Debe ingresar la cantidad")
            if not precio_unitario:
                errores.append("Debe ingresar el precio unitario")
            
            if errores:
                flash('. '.join(errores), 'error')
                return redirect(url_for('ordenes_compra_page'))
            
            # Convertir a tipos correctos
            proveedor_id = int(proveedor_id)
            medicamento_id = int(medicamento_id)
            cantidad = int(cantidad)
            precio_unitario = float(precio_unitario)
            observaciones = request.form.get('observaciones', '').strip() or None
            
            total = cantidad * precio_unitario
            
            logger.info(f"Registrando orden: proveedor={proveedor_id}, medicamento={medicamento_id}, cantidad={cantidad}, precio={precio_unitario}, total={total}")
            
            # Insertar orden de compra
            result = mysql_models.registrar_orden_compra(
                proveedor_id=proveedor_id,
                medicamento_id=medicamento_id,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                total=total,
                observaciones=observaciones
            )
            
            logger.info(f"Resultado de registrar_orden_compra: {result}")
            
            if result['success']:
                flash('Orden de compra registrada exitosamente', 'success')
                return redirect(url_for('ordenes_compra_page'))
            else:
                flash(f'Error al registrar orden: {result["mensaje"]}', 'error')
                return redirect(url_for('ordenes_compra_page'))
                
        except Exception as e:
            logger.error(f"Error al registrar orden: {e}")
            logger.error(traceback.format_exc())
            flash(f'Error al procesar orden: {str(e)}', 'error')
            return redirect(url_for('ordenes_compra_page'))
    
    # GET - Mostrar página con lógica paso a paso
    proveedor_id = request.args.get('proveedor_id', type=int)
    medicamento_id = request.args.get('medicamento_id', type=int)
    cantidad = request.args.get('cantidad', type=int)
    
    proveedor_seleccionado = None
    medicamentos_proveedor = []
    medicamento_seleccionado = None
    precio_calculado = None
    
    # Paso 1: Si hay proveedor, cargar sus datos y medicamentos
    if proveedor_id:
        proveedores = mysql_models.get_all_proveedores()
        proveedor_seleccionado = next((p for p in proveedores if p['id'] == proveedor_id), None)
        
        if proveedor_seleccionado:
            medicamentos_proveedor = mysql_models.get_medicamentos_por_proveedor(proveedor_id)
    
    # Paso 2: Si hay medicamento, cargar sus datos
    if medicamento_id and medicamentos_proveedor:
        medicamento_seleccionado = next(
            (m for m in medicamentos_proveedor if m['id_medicamento'] == medicamento_id), 
            None
        )
    
    # Paso 3: Si hay cantidad, calcular precio con descuento
    if proveedor_id and medicamento_id and cantidad and cantidad > 0:
        precio_info = mysql_models.get_precio_proveedor(proveedor_id, medicamento_id, cantidad)
        if precio_info:
            precio_calculado = precio_info[0]
    
    # GET - Mostrar página
    try:
        # Obtener estadísticas
        stats = mysql_models.get_ordenes_stats()
        
        # Obtener datos para selects
        proveedores = mysql_models.get_all_proveedores()
        medicamentos = mysql_models.get_all_medicamentos()
        
        # Obtener órdenes recientes
        ordenes = mysql_models.get_ordenes_recientes()
        
        # Obtener mensaje flash si existe
        mensaje = None
        mensaje_tipo = None
        if '_flashes' in session:
            flashes = session.get('_flashes', [])
            if flashes:
                mensaje_tipo, mensaje = flashes[0]
        
        return render_template('ordenes_compra.html',
                             ordenes=ordenes,
                             proveedores=proveedores,
                             medicamentos=medicamentos,
                             proveedor_seleccionado=proveedor_seleccionado,
                             medicamentos_proveedor=medicamentos_proveedor,
                             medicamento_seleccionado=medicamento_seleccionado,
                             precio_calculado=precio_calculado,
                             cantidad_ingresada=cantidad,
                             mensaje=mensaje,
                             mensaje_tipo=mensaje_tipo,
                             ordenes_pendientes=stats.get('ordenes_pendientes', 0),
                             ordenes_mes=stats.get('ordenes_mes', 0),
                             total_mes=stats.get('total_mes', 0),
                             proveedores_activos=stats.get('proveedores_activos', 0))
    except Exception as e:
        print(f"Error al cargar órdenes: {e}")
        return render_template('ordenes_compra.html', ordenes=[], proveedores=[], medicamentos=[])

@app.route('/api/ordenes-compra/estado/<int:orden_id>', methods=['POST'])
@login_required
@role_required('Gerente')
def actualizar_estado_orden(orden_id):
    # Actualizar estado de orden de compra
    try:
        nuevo_estado = request.form.get('estado')
        if not nuevo_estado or nuevo_estado not in ['Pendiente', 'Aprobada', 'Recibida', 'Cancelada']:
            return jsonify({'success': False, 'mensaje': 'Estado inválido'}), 400
        
        result = mysql_models.update_orden_estado(orden_id, nuevo_estado)
        
        if result['success']:
            flash(result['mensaje'], 'success')
            return jsonify(result), 200
        else:
            flash(result['mensaje'], 'error')
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"Error al actualizar estado: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'mensaje': str(e)}), 500

@app.route('/api/proveedores')
@login_required
def get_proveedores():
    # Obtener lista de proveedores
    proveedores = mysql_models.get_all_proveedores()
    return jsonify(proveedores)


@app.route('/ensayos-clinicos', methods=['GET', 'POST'])
@login_required
@role_required('Gerente', 'Investigador')
def ensayos_clinicos_page():
    # Página de ensayos clínicos
    if request.method == 'POST':
        # Procesar nuevo ensayo clínico
        try:
            logger.info(f"Creando ensayo clínico. Form data: {request.form}")
            
            trial_data = {
                'trial_id': request.form.get('trial_id', '').strip(),
                'titulo': request.form.get('titulo', '').strip(),
                'medicamento_id': int(request.form.get('medicamento_id', 0)),
                'medicamento_nombre': request.form.get('medicamento_nombre', '').strip(),
                'fase': request.form.get('fase', '').strip(),
                'estado': request.form.get('estado', 'En Curso').strip(),
                'fecha_inicio': request.form.get('fecha_inicio', '').strip(),
                'objetivo_principal': request.form.get('objetivo_principal', 'No especificado').strip(),
                'creado_por': session.get('username', 'Sistema')
            }
            
            # Validar que los campos requeridos no estén vacíos
            if not all([trial_data['trial_id'], trial_data['titulo'], trial_data['medicamento_nombre'], trial_data['fase'], trial_data['fecha_inicio']]):
                flash('Todos los campos marcados con * son obligatorios', 'error')
                # Obtener datos para re-renderizar el formulario
                ensayos = mongodb_models.get_all_clinical_trials()
                medicamentos = mysql_models.get_all_medicamentos()
                total_ensayos = len(ensayos)
                ensayos_activos = len([e for e in ensayos if e.get('estado') == 'En Curso'])
                investigadores = set()
                for ensayo in ensayos:
                    if 'investigadores' in ensayo:
                        for inv in ensayo['investigadores']:
                            investigadores.add(inv.get('nombre', ''))
                return render_template('ensayos_clinicos.html', 
                                     ensayos=ensayos,
                                     medicamentos=medicamentos,
                                     total_ensayos=total_ensayos,
                                     ensayos_activos=ensayos_activos,
                                     total_investigadores=len(investigadores))
            
            # Usar la función del modelo
            result = mongodb_models.create_clinical_trial(trial_data)
            logger.info(f"Resultado crear ensayo: {result}")
            
            if result['success']:
                flash('Ensayo clínico registrado exitosamente', 'success')
                return redirect(url_for('ensayos_clinicos_page'))
            else:
                flash(f'Error: {result["mensaje"]}', 'error')
                # Obtener datos para re-renderizar el formulario
                ensayos = mongodb_models.get_all_clinical_trials()
                medicamentos = mysql_models.get_all_medicamentos()
                total_ensayos = len(ensayos)
                ensayos_activos = len([e for e in ensayos if e.get('estado') == 'En Curso'])
                investigadores = set()
                for ensayo in ensayos:
                    if 'investigadores' in ensayo:
                        for inv in ensayo['investigadores']:
                            investigadores.add(inv.get('nombre', ''))
                return render_template('ensayos_clinicos.html', 
                                     ensayos=ensayos,
                                     medicamentos=medicamentos,
                                     total_ensayos=total_ensayos,
                                     ensayos_activos=ensayos_activos,
                                     total_investigadores=len(investigadores))
                
        except Exception as e:
            logger.error(f"Error al registrar ensayo: {e}")
            logger.error(traceback.format_exc())
            flash(f'Error al crear ensayo: {str(e)}', 'error')
            # Obtener datos para re-renderizar el formulario
            ensayos = mongodb_models.get_all_clinical_trials()
            medicamentos = mysql_models.get_all_medicamentos()
            total_ensayos = len(ensayos)
            ensayos_activos = len([e for e in ensayos if e.get('estado') == 'En Curso'])
            investigadores = set()
            for ensayo in ensayos:
                if 'investigadores' in ensayo:
                    for inv in ensayo['investigadores']:
                        investigadores.add(inv.get('nombre', ''))
            return render_template('ensayos_clinicos.html', 
                                 ensayos=ensayos,
                                 medicamentos=medicamentos,
                                 total_ensayos=total_ensayos,
                                 ensayos_activos=ensayos_activos,
                                 total_investigadores=len(investigadores))
    
    # GET - Mostrar página
    try:
        # Obtener todos los ensayos clínicos usando el modelo
        ensayos = mongodb_models.get_all_clinical_trials()
        logger.info(f"Total ensayos obtenidos: {len(ensayos)}")
        
        # Obtener lista de medicamentos para el dropdown
        medicamentos = mysql_models.get_all_medicamentos()
        logger.info(f"Total medicamentos obtenidos para dropdown: {len(medicamentos)}")
        if medicamentos:
            logger.info(f"Primer medicamento: {medicamentos[0]}")
        
        # Calcular estadísticas
        total_ensayos = len(ensayos)
        ensayos_activos = len([e for e in ensayos if e.get('estado') == 'En Curso'])
        
        # Contar investigadores únicos
        investigadores = set()
        for ensayo in ensayos:
            if 'investigadores' in ensayo:
                for inv in ensayo['investigadores']:
                    investigadores.add(inv.get('nombre', ''))
        
        return render_template('ensayos_clinicos.html', 
                             ensayos=ensayos,
                             medicamentos=medicamentos,
                             total_ensayos=total_ensayos,
                             ensayos_activos=ensayos_activos,
                             total_investigadores=len(investigadores))
    except Exception as e:
        logger.error(f"Error al cargar ensayos clínicos: {e}")
        logger.error(traceback.format_exc())
        return render_template('ensayos_clinicos.html', 
                             ensayos=[], 
                             total_ensayos=0,
                             ensayos_activos=0,
                             total_investigadores=0)

@app.route('/api/ensayo-clinico/<trial_id>')
@login_required
@role_required('Gerente', 'Investigador')
def get_ensayo_clinico(trial_id):
    # Obtener detalle de un ensayo clínico
    ensayo = mongodb_models.get_clinical_trial_by_id(trial_id)
    if not ensayo:
        return jsonify({'error': 'Ensayo no encontrado'}), 404
    return jsonify(ensayo)

@app.route('/api/ensayo-clinico/<trial_id>', methods=['PUT'])
@login_required
@role_required('Investigador')
def update_ensayo_clinico(trial_id):
    # Actualizar ensayo clínico
    data = request.get_json()
    result = mongodb_models.update_clinical_trial(trial_id, data)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify({'error': result['mensaje']}), 400


@app.route('/reportes')
@login_required
def reportes_page():
    # Página de reportes
    # Obtener estadísticas para los reportes
    try:
        # Contar medicamentos y lotes
        medicamentos = mysql_models.get_all_medicamentos()
        lotes = mysql_models.get_all_lotes()
        
        # Datos de MongoDB
        ensayos = mongodb_models.get_all_clinical_trials()
        
        data = {
            'total_medicamentos': len(medicamentos) if medicamentos else 0,
            'lotes_activos': len(lotes) if lotes else 0,
            'alertas_stock': len([m for m in medicamentos if m.get('stock_actual', 0) < m.get('stock_minimo', 0)]) if medicamentos else 0,
            'ensayos_activos': len([e for e in ensayos if e.get('estado') == 'En Curso']),
            'ventas_mes': 'N/A',
            'ingresos_totales': '0.00',
            'clientes_activos': 'N/A',
            'vencen_30_dias': 'N/A',
            'vencen_60_dias': 'N/A',
            'ya_vencidos': 'N/A',
            'ordenes_mes': 'N/A',
            'proveedores_activos': 'N/A',
            'gastos_totales': '0.00',
            'transacciones_hoy': 'N/A',
            'usuarios_activos': 'N/A',
            'ultima_auditoria': 'N/A'
        }
    except Exception as e:
        # Si hay error, usar valores por defecto
        data = {
            'total_medicamentos': 'N/A',
            'lotes_activos': 'N/A',
            'alertas_stock': 'N/A',
            'ensayos_activos': 'N/A',
            'reportes_publicados': 'N/A',
            'eventos_adversos': 'N/A',
            'ventas_mes': 'N/A',
            'ingresos_totales': '0.00',
            'clientes_activos': 'N/A',
            'vencen_30_dias': 'N/A',
            'vencen_60_dias': 'N/A',
            'ya_vencidos': 'N/A',
            'ordenes_mes': 'N/A',
            'proveedores_activos': 'N/A',
            'gastos_totales': '0.00',
            'transacciones_hoy': 'N/A',
            'usuarios_activos': 'N/A',
            'ultima_auditoria': 'N/A'
        }
    
    return render_template('reportes.html', **data)

@app.route('/api/estadisticas/ventas')
@login_required
@role_required('Gerente')
def estadisticas_ventas():
    # Estadísticas de ventas
    stats = mysql_models.get_estadisticas_ventas()
    return jsonify(stats)

@app.route('/api/estadisticas/inventario')
@login_required
def estadisticas_inventario():
    # Estadísticas de inventario
    stats = mysql_models.get_estadisticas_inventario()
    return jsonify(stats)

@app.route('/api/auditoria')
@login_required
@role_required('Gerente')
def get_auditoria():
    # Obtener registros de auditoría
    limit = request.args.get('limit', 100, type=int)
    auditoria = mysql_models.get_auditoria(limit)
    return jsonify(auditoria)


@app.route('/usuarios', methods=['GET', 'POST'])
@login_required
@role_required('Gerente')
def usuarios_page():
    # Página de gestión de usuarios
    if request.method == 'POST':
        # Procesar nuevo usuario
        try:
            nombre = request.form.get('nombre')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            rol = request.form.get('rol')
            telefono = request.form.get('telefono') or None
            
            # Encriptar contraseña
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insertar usuario
            result = mysql_models.registrar_usuario(
                nombre=nombre,
                email=email,
                username=username,
                password_hash=password_hash,
                rol=rol,
                telefono=telefono
            )
            
            if result['success']:
                return redirect(url_for('usuarios_page'))
            else:
                return render_template('usuarios.html', mensaje=result['mensaje'], mensaje_tipo='error')
                
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return render_template('usuarios.html', mensaje=f'Error: {str(e)}', mensaje_tipo='error')
    
    # GET - Mostrar página
    try:
        # Obtener todos los usuarios
        usuarios = mysql_models.get_all_usuarios()
        
        # Obtener estadísticas
        stats = mysql_models.get_usuarios_stats()
        
        return render_template('usuarios.html',
                             usuarios=usuarios,
                             total_usuarios=stats.get('total_usuarios', 0),
                             total_gerentes=stats.get('total_gerentes', 0),
                             total_farmaceuticos=stats.get('total_farmaceuticos', 0),
                             total_investigadores=stats.get('total_investigadores', 0))
    except Exception as e:
        print(f"Error al cargar usuarios: {e}")
        return render_template('usuarios.html', usuarios=[])

@app.route('/api/usuario/<int:id>', methods=['PUT'])

@app.errorhandler(403)
def forbidden(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Acceso denegado'}), 403
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint no encontrado'}), 404
    return render_template('404.html'), 404

@app.route('/api/lotes-caducados', methods=['GET'])
@login_required
@role_required('Gerente', 'Farmacéutico')
def get_lotes_caducados():
    # Obtener lista de lotes caducados
    try:
        lotes = mysql_models.get_lotes_caducados()
        return jsonify(lotes)
    except Exception as e:
        logger.error(f"Error obteniendo lotes caducados: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/lotes/<int:lote_id>/eliminar', methods=['POST'])
@login_required
@role_required('Gerente')
def eliminar_lote(lote_id):
    # Eliminar un lote caducado
    try:
        result = mysql_models.eliminar_lote_caducado(lote_id)
        if result:
            return jsonify({'success': True, 'message': 'Lote eliminado correctamente'})
        return jsonify({'success': False, 'message': 'No se pudo eliminar el lote'}), 400
    except Exception as e:
        logger.error(f"Error eliminando lote: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicamentos/nuevo', methods=['POST'])
@login_required
@role_required('Gerente', 'Farmacéutico')
def crear_medicamento_nuevo():
    # Crear un nuevo medicamento
    try:
        data = request.get_json()
        
        nombre = data.get('nombre')
        principio_activo = data.get('principio_activo')
        id_categoria = data.get('id_categoria')
        descripcion = data.get('descripcion')
        indicaciones = data.get('indicaciones')
        contraindicaciones = data.get('contraindicaciones')
        dosis_recomendada = data.get('dosis_recomendada')
        
        if not all([nombre, principio_activo, id_categoria]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        medicamento_id = mysql_models.crear_medicamento(
            nombre, principio_activo, id_categoria, 
            descripcion, indicaciones, contraindicaciones, dosis_recomendada
        )
        
        if medicamento_id:
            return jsonify({'success': True, 'message': 'Medicamento creado', 'id': medicamento_id})
        return jsonify({'success': False, 'message': 'No se pudo crear el medicamento'}), 400
        
    except Exception as e:
        logger.error(f"Error creando medicamento: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias', methods=['GET'])
@login_required
def get_categorias():
    # Obtener todas las categorías
    try:
        categorias = mysql_models.get_all_categorias()
        return jsonify(categorias)
    except Exception as e:
        logger.error(f"Error obteniendo categorías: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Error 500 en {request.path}: {str(e)}")
    logger.error(traceback.format_exc())
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500
    return render_template('404.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Excepción no manejada en {request.path}: {str(e)}")
    logger.error(traceback.format_exc())
    if request.path.startswith('/api/'):
        return jsonify({'error': str(e)}), 500
    flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    print("PHARMAFLOW SOLUTIONS - Sistema iniciando...")
    print(f"Modo: {'Desarrollo' if Config.DEBUG else 'Produccion'}")
    print(f"Puerto: {Config.PORT}")
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
