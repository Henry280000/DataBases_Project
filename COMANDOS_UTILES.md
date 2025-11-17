#  COMANDOS ÚTILES - PHARMAFLOW SOLUTIONS

##  Inicio Rápido

```bash
# Instalar todo automáticamente
./install.sh

# Iniciar aplicación
./start.sh

# O manualmente:
source venv/bin/activate
python app.py
```

## Comandos MySQL

### Conectarse
```bash
# Como root
mysql -u root -p

# Como usuario de aplicación
mysql -u pharmaflow_app -p -D pharmaflow_relational
# Password: AppPharma2024!
```

### Consultas Útiles
```sql
-- Ver inventario actual
SELECT * FROM v_inventario_actual LIMIT 10;

-- Ver medicamentos próximos a caducar
SELECT * FROM v_medicamentos_por_caducar;

-- Ver últimas ventas
SELECT v.*, c.nombre AS cliente 
FROM ventas v 
LEFT JOIN clientes c ON v.id_cliente = c.id_cliente 
ORDER BY v.fecha_venta DESC 
LIMIT 10;

-- Ver auditoría reciente
SELECT * FROM auditoria_transacciones 
ORDER BY fecha_operacion DESC 
LIMIT 20;

-- Valor total del inventario
SELECT fn_valor_inventario_total() AS valor_total;

-- Actualizar lotes caducados
CALL sp_actualizar_lotes_caducados();

-- Ver privilegios de un usuario
SHOW GRANTS FOR 'gerente_user'@'localhost';
```

### Administración
```sql
-- Ver usuarios
SELECT User, Host FROM mysql.user;

-- Ver bases de datos
SHOW DATABASES;

-- Ver tablas
USE pharmaflow_relational;
SHOW TABLES;

-- Ver estructura de tabla
DESCRIBE lotes;

-- Ver índices de una tabla
SHOW INDEX FROM lotes;

-- Ver procedimientos almacenados
SHOW PROCEDURE STATUS WHERE Db = 'pharmaflow_relational';

-- Ver triggers
SHOW TRIGGERS;
```

##  Comandos MongoDB

### Conectarse
```bash
# Sin autenticación
mongosh

# Con autenticación
mongosh -u pharmaflow_app -p AppMongo2024! --authenticationDatabase admin
```

### Consultas Útiles
```javascript
// Cambiar a base de datos
use pharmaflow_nosql

// Ver colecciones
show collections

// Ver todos los ensayos clínicos
db.clinical_trials.find().pretty()

// Buscar ensayo específico
db.clinical_trials.findOne({ trial_id: "CT-2024-001" })

// Buscar ensayos por estado
db.clinical_trials.find({ estado: "En Curso" })

// Buscar ensayos por medicamento
db.clinical_trials.find({ medicamento_id: 4 })

// Contar ensayos
db.clinical_trials.countDocuments()

// Ver reportes de un ensayo
db.research_reports.find({ trial_id: "CT-2024-001" })

// Ver eventos adversos por severidad
db.adverse_events.find({ severidad: "Severo" })

// Buscar interacción de compuestos
db.compound_interactions.find({
  $or: [
    { "compuesto_a.nombre": /Amoxicilina/i },
    { "compuesto_b.nombre": /Amoxicilina/i }
  ]
})

// Estadísticas de eventos adversos
db.adverse_events.aggregate([
  { $group: { 
    _id: "$severidad", 
    count: { $sum: 1 } 
  }}
])

// Ver índices
db.clinical_trials.getIndexes()
```

### Administración MongoDB
```javascript
// Ver usuarios
use admin
db.getUsers()

// Ver estadísticas de la BD
db.stats()

// Ver colecciones con tamaño
db.getCollectionNames().forEach(function(col) {
  print(col + ": " + db[col].countDocuments() + " documentos");
})

// Validar colección
db.clinical_trials.validate()
```

## Pruebas con API

### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_gerente",
    "password": "PharmaFlow123!"
  }'
```

### Ver Inventario
```bash
curl http://localhost:5000/api/inventario \
  -H "Cookie: session=..."
```

### Registrar Venta
```bash
curl -X POST http://localhost:5000/api/ventas \
  -H "Content-Type: application/json" \
  -H "Cookie: session=..." \
  -d '{
    "id_cliente": 1,
    "metodo_pago": "Efectivo",
    "detalles": [
      {
        "id_lote": 1,
        "cantidad": 5,
        "precio": 5.50
      }
    ]
  }'
```

### Ver Ensayos Clínicos
```bash
curl http://localhost:5000/api/ensayos-clinicos \
  -H "Cookie: session=..."
```

##  Mantenimiento

### Backup MySQL
```bash
# Backup completo
mysqldump -u root -p pharmaflow_relational > backup_$(date +%Y%m%d).sql

# Backup solo estructura
mysqldump -u root -p --no-data pharmaflow_relational > schema_backup.sql

# Backup solo datos
mysqldump -u root -p --no-create-info pharmaflow_relational > data_backup.sql
```

### Restaurar MySQL
```bash
mysql -u root -p pharmaflow_relational < backup_20241113.sql
```

### Backup MongoDB
```bash
# Backup completo
mongodump --db pharmaflow_nosql --out backup_mongo_$(date +%Y%m%d)

# Backup de una colección
mongodump --db pharmaflow_nosql --collection clinical_trials --out backup_trials
```

### Restaurar MongoDB
```bash
mongorestore --db pharmaflow_nosql backup_mongo_20241113/pharmaflow_nosql
```

##  Gestión de Dependencias

```bash
# Ver dependencias instaladas
pip list

# Actualizar una dependencia
pip install --upgrade Flask

# Reinstalar todas las dependencias
pip install --force-reinstall -r requirements.txt

# Verificar dependencias
pip check
```

## Debugging

### Ver logs de MySQL
```bash
# macOS
tail -f /opt/homebrew/var/mysql/*.err

# Linux
tail -f /var/log/mysql/error.log
```

### Ver logs de MongoDB
```bash
# macOS
tail -f /opt/homebrew/var/log/mongodb/mongo.log

# Linux
tail -f /var/log/mongodb/mongod.log
```

### Ver logs de Python
```bash
tail -f logs/pharmaflow.log
```

### Probar conexión MySQL desde Python
```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='pharmaflow_app',
    password='AppPharma2024!',
    database='pharmaflow_relational'
)

cursor = conn.cursor()
cursor.execute("SELECT DATABASE();")
print(cursor.fetchone())
conn.close()
```

### Probar conexión MongoDB desde Python
```python
from pymongo import MongoClient

client = MongoClient('mongodb://pharmaflow_app:AppMongo2024!@localhost:27017/')
db = client.pharmaflow_nosql

print(db.list_collection_names())
print(db.clinical_trials.count_documents({}))
```

##  Monitoreo

### Ver procesos MySQL
```sql
SHOW PROCESSLIST;

-- Ver procesos de un usuario específico
SELECT * FROM information_schema.PROCESSLIST 
WHERE USER = 'pharmaflow_app';
```

### Ver conexiones activas
```sql
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
```

### Ver tamaño de tablas
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.TABLES
WHERE table_schema = 'pharmaflow_relational'
ORDER BY size_mb DESC;
```

### Estadísticas MongoDB
```javascript
// Tamaño de la base de datos
db.stats()

// Operaciones en curso
db.currentOp()

// Estado del servidor
db.serverStatus()
```

## ⚙ Configuración

### Cambiar puerto de Flask
```python
# En app.py o crear variable de entorno
export PORT=8000
python app.py
```

### Variables de entorno
```bash
# Crear archivo .env
cat > .env << EOF
SECRET_KEY=mi-clave-super-secreta
MYSQL_HOST=localhost
MYSQL_USER=pharmaflow_app
MYSQL_PASSWORD=AppPharma2024!
PORT=5000
DEBUG=True
EOF
```

### Reiniciar servicios
```bash
# MySQL
brew services restart mysql

# MongoDB
brew services restart mongodb-community

# Python (Ctrl+C y reiniciar)
python app.py
```

##  Consultas de Análisis

### Top 10 medicamentos más vendidos
```sql
SELECT 
    m.nombre,
    SUM(dv.cantidad) AS total_vendido,
    SUM(dv.subtotal) AS ingresos_totales
FROM detalles_venta dv
JOIN lotes l ON dv.id_lote = l.id_lote
JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
GROUP BY m.id_medicamento
ORDER BY total_vendido DESC
LIMIT 10;
```

### Ventas por mes
```sql
SELECT 
    DATE_FORMAT(fecha_venta, '%Y-%m') AS mes,
    COUNT(*) AS num_ventas,
    SUM(total) AS monto_total
FROM ventas
WHERE estado = 'Completada'
GROUP BY mes
ORDER BY mes DESC;
```

### Inventario con valor
```sql
SELECT 
    c.nombre AS categoria,
    COUNT(DISTINCT l.id_lote) AS num_lotes,
    SUM(l.cantidad_actual) AS unidades,
    SUM(l.cantidad_actual * l.precio_unitario) AS valor_total
FROM lotes l
JOIN medicamentos m ON l.id_medicamento = m.id_medicamento
JOIN categorias c ON m.id_categoria = c.id_categoria
WHERE l.estado = 'Disponible'
GROUP BY c.id_categoria
ORDER BY valor_total DESC;
```
