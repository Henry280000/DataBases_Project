# CÓMO EJECUTAR PHARMAFLOW SOLUTIONS

## Guía Rápida de Ejecución

---

## OPCIÓN 1: INSTALACIÓN AUTOMÁTICA (Recomendada)

### Paso 1: Ejecutar el instalador

```bash
cd "/Users/enrique/Documents/Programacion/proyecto 2 bases de datos"
./install.sh
```

### Paso 2: Seguir las instrucciones

El script te preguntará:
```
¿Usuario root de MySQL? [root]: root
¿Contraseña root de MySQL?: tu_contraseña
```

### Paso 3: Esperar a que termine

El instalador hará automáticamente:
- Crear entorno virtual
- Instalar todas las dependencias Python
- Crear base de datos MySQL
- Configurar MongoDB (con Python)
- Cargar datos iniciales

### Paso 4: Iniciar la aplicación

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar aplicación
python app.py
```

O usar el script de inicio:
```bash
./start.sh
```

---

## OPCIÓN 2: INSTALACIÓN MANUAL

Si prefieres hacer todo paso a paso:

### 1. Crear entorno virtual

```bash
cd "/Users/enrique/Documents/Programacion/proyecto 2 bases de datos"
python3 -m venv venv
```

### 2. Activar entorno virtual

```bash
source venv/bin/activate
```

Verás que tu terminal cambia a:
```
(venv) usuario@mac proyecto 2 bases de datos %
```

### 3. Instalar dependencias

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0
- Flask-CORS 4.0.0
- pymongo 4.6.0
- mysql-connector-python 8.2.0
- bcrypt 4.1.1
- gunicorn 21.2.0

### 4. Configurar MySQL

```bash
# Opción A: Con usuario root
mysql -u root -p < database/mysql_schema.sql
mysql -u root -p < database/mysql_roles_privileges.sql
mysql -u root -p < database/mysql_data_seed.sql

# Opción B: Con otro usuario
mysql -u tu_usuario -p < database/mysql_schema.sql
mysql -u tu_usuario -p < database/mysql_roles_privileges.sql
mysql -u tu_usuario -p < database/mysql_data_seed.sql
```

### 5. Verificar que MongoDB esté corriendo

```bash
# Verificar si está corriendo
brew services list | grep mongodb

# Si no está corriendo, iniciarlo
brew services start mongodb-community
```

### 6. Configurar MongoDB (Python)

```bash
# Configuración (crea colecciones, índices, usuario)
python database/mongodb_setup.py

# Datos iniciales (carga ensayos clínicos, reportes, etc.)
python database/mongodb_seed.py
```

### 7. Iniciar la aplicación

```bash
python app.py
```

O con Flask:
```bash
flask run
```

---

## VERIFICACIÓN

### Comprobar que todo está instalado

```bash
# Verificar entorno virtual activo
which python
# Debe mostrar: .../proyecto 2 bases de datos/venv/bin/python

# Verificar dependencias
pip list | grep -E "(Flask|pymongo|mysql|bcrypt)"
```

Debes ver:
```
bcrypt                4.1.1
Flask                 3.0.0
Flask-Cors            4.0.0
mysql-connector-python 8.2.0
pymongo               4.6.0
```

### Comprobar MySQL

```bash
mysql -u pharmaflow_app -pAppPharma2024! -e "USE pharmaflow_relational; SHOW TABLES;"
```

Debes ver las tablas:
```
auditoria_medicamentos
clientes
compras
detalle_compras
detalle_ventas
laboratorios
lotes
medicamentos
ordenes_compra
proveedores
usuarios
ventas
```

### Comprobar MongoDB

```bash
python -c "
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['pharmaflow_nosql']
print('Colecciones:', db.list_collection_names())
print('Ensayos clínicos:', db.clinical_trials.count_documents({}))
"
```

Debes ver:
```
Colecciones: ['clinical_trials', 'research_reports', 'adverse_events', 'compound_interactions']
Ensayos clínicos: 3
```

---

## ACCEDER A LA APLICACIÓN

### 1. Abrir navegador

```
http://localhost:5000
```

O:
```
http://127.0.0.1:5000
```

### 2. Iniciar sesión

Usuarios de prueba disponibles:

#### Gerente (acceso total)
```
Usuario: admin_gerente
Contraseña: PharmaFlow123!
```

#### Farmacéutico (ventas e inventario)
```
Usuario: maria_farm
Contraseña: PharmaFlow123!
```

#### Investigador (solo ensayos clínicos)
```
Usuario: ana_investigadora
Contraseña: PharmaFlow123!
```

---

## COMANDOS ÚTILES

### Iniciar aplicación (con entorno virtual activo)

```bash
python app.py
```

### Detener aplicación

```
Ctrl + C
```

### Reiniciar MongoDB

```bash
brew services restart mongodb-community
```

### Reiniciar MySQL

```bash
brew services restart mysql
```

### Ver logs

```bash
tail -f logs/pharmaflow.log
```

### Recargar datos de MongoDB

```bash
# Solo si quieres limpiar y recargar todo
python database/mongodb_seed.py
```

---

## SOLUCIÓN DE PROBLEMAS

### Error: "ModuleNotFoundError: No module named 'bcrypt'"

**Solución:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL server"

**Solución:**
```bash
# Verificar que MySQL esté corriendo
brew services list | grep mysql

# Iniciar MySQL si no está corriendo
brew services start mysql
```

### Error: "Authentication failed" (MongoDB)

**Solución:**
```bash
# Reconfigurar MongoDB
python database/mongodb_setup.py
```

### Error: "Port 5000 is already in use"

**Solución:**
```bash
# Encontrar el proceso usando el puerto
lsof -ti:5000

# Matar el proceso
kill -9 $(lsof -ti:5000)

# O usar otro puerto
flask run --port 5001
```

### Error: "Access denied for user 'pharmaflow_app'"

**Solución:**
```bash
# Recrear el usuario de MySQL
mysql -u root -p < database/mysql_roles_privileges.sql
```

---

## SCRIPTS DE AYUDA

### Script de inicio rápido (start.sh)

Ya existe en tu proyecto:
```bash
./start.sh
```

Este script:
1. Verifica que MongoDB esté corriendo
2. Activa el entorno virtual
3. Inicia la aplicación Flask

### Script de instalación (install.sh)

```bash
./install.sh
```

Instala y configura todo automáticamente.

---

## DESARROLLO

### Modo Debug

Para desarrollo con auto-reload:

```bash
export FLASK_ENV=development
python app.py
```

O editar `app.py` (última línea):
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Cambiar puerto

```bash
# Opción 1: Editar app.py
# Cambiar: app.run(port=5000)
# A: app.run(port=8080)

# Opción 2: Variable de entorno
export PORT=8080
python app.py
```

---

## RESUMEN RÁPIDO

```bash
# INICIO RÁPIDO (después de instalar)
cd "/Users/enrique/Documents/Programacion/proyecto 2 bases de datos"
source venv/bin/activate
python app.py

# Abrir navegador en: http://localhost:5000
# Login: admin_gerente / PharmaFlow123!
```

---

## ESTRUCTURA DEL PROYECTO

```
proyecto 2 bases de datos/
├── app.py                    ← Archivo principal (ejecutar este)
├── requirements.txt          ← Dependencias Python
├── install.sh               ← Instalador automático
├── start.sh                 ← Iniciador rápido
├── venv/                    ← Entorno virtual (crear con: python3 -m venv venv)
├── config/
│   └── config.py            ← Configuración (MySQL, MongoDB)
├── database/
│   ├── mysql_schema.sql     ← Schema MySQL
│   ├── mysql_roles_privileges.sql  ← Usuarios MySQL
│   ├── mysql_data_seed.sql  ← Datos MySQL
│   ├── mongodb_setup.py     ← Configuración MongoDB (Python)
│   └── mongodb_seed.py      ← Datos MongoDB (Python)
├── models/                  ← ORM/ODM manual
├── utils/                   ← Utilidades (seguridad, helpers)
├── templates/               ← HTML (Jinja2)
└── static/                  ← CSS
```

---

## CHECKLIST DE INSTALACIÓN

- [ ] Python 3.8+ instalado
- [ ] MySQL 8.0+ instalado y corriendo
- [ ] MongoDB 6.0+ instalado y corriendo
- [ ] Entorno virtual creado (`python3 -m venv venv`)
- [ ] Entorno virtual activado (`source venv/bin/activate`)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] MySQL configurado (scripts .sql ejecutados)
- [ ] MongoDB configurado (`python database/mongodb_setup.py`)
- [ ] Datos cargados (`python database/mongodb_seed.py`)
- [ ] Aplicación iniciada (`python app.py`)
- [ ] Navegador abierto en `http://localhost:5000`
- [ ] Login exitoso con usuario de prueba

---

**¡Todo listo! Tu aplicación debería estar corriendo en http://localhost:5000**
