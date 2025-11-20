#  PharmaFlow Solutions

Sistema integral de gestión farmacéutica con base de datos híbrida (MySQL + MongoDB)

##  Descripción del Proyecto

PharmaFlow Solutions es un sistema robusto diseñado para empresas farmacéuticas que necesitan:

- ** Gestión de Inventario** (MySQL): Control de medicamentos, lotes, caducidades
- ** Transacciones** (MySQL): Ventas y órdenes de compra con control de concurrencia
- ** Ensayos Clínicos** (MongoDB): Documentación flexible de investigación
- ** Control de Usuarios**: Sistema de roles (Gerente, Farmacéutico, Investigador)

##  Arquitectura del Sistema

### Base de Datos Relacional (MySQL)
- Control de inventario y transacciones
- Procedimientos almacenados para venta con control de concurrencia optimista
- Triggers para auditoría automática
- Vistas optimizadas para consultas frecuentes

### Base de Datos NoSQL (MongoDB)
- Ensayos clínicos con estructura flexible
- Reportes de investigación
- Eventos adversos
- Interacciones de compuestos químicos

### Backend (Python + Flask)
- API RESTful
- ORM/ODM manual para mapeo de objetos
- Gestión de sesiones y autenticación
- Control de acceso basado en roles

### Frontend (HTML + CSS + JavaScript)
- Interfaz responsive
- Dashboard interactivo
- Gestión de ventas e inventario
- Consulta de ensayos clínicos

##  Instalación

### Windows

**Guía completa**: Ver [INSTALACION_WINDOWS.md](INSTALACION_WINDOWS.md)

**Instalación rápida**:
1. Haz clic derecho en `install.bat` → "Ejecutar como administrador"
2. Doble click en `start.bat`
3. Abre http://localhost:5001

### Linux / macOS

**Guía completa**: Ver [INSTALACION.md](INSTALACION.md)

**Instalación rápida**:
```bash
# Verificar requisitos
chmod +x check_requirements.sh
./check_requirements.sh

# Instalar
chmod +x install.sh
./install.sh

# Iniciar
chmod +x start.sh
./start.sh
```

O manualmente:
```bash
source venv/bin/activate
python app.py
```

### Requisitos del Sistema

```bash
# Python 3.9+
python3 --version

# MySQL 8.0+
mysql --version

# MongoDB 6.0+
mongosh --version
```

### 1. Clonar o Descargar el Proyecto

```bash
cd "proyecto 2 bases de datos"
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
```

### 3. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

```bash
# Conectarse a MySQL
mysql -u root -p

# Ejecutar scripts en orden
source database/mysql_schema.sql
source database/mysql_roles_privileges.sql
source database/mysql_data_seed.sql
```

**Nota sobre usuarios:** Los scripts crean usuarios con contraseñas predefinidas:
- `pharmaflow_app` / `AppPharma2024!`
- `gerente_user` / `Gerente2024!`
- `farmaceutico_user` / `Farmaceutico2024!`
- `investigador_user` / `Investigador2024!`

### 5. Configurar MongoDB

```bash
# Iniciar MongoDB (si no está corriendo)
brew services start mongodb-community

# Conectarse a MongoDB
mongosh

# Ejecutar scripts de configuración
load('database/mongodb_setup.js')
load('database/mongodb_seed.js')
```

**Nota:** Si MongoDB requiere autenticación, editar `config/config.py` con las credenciales correctas.

### 6. Configurar Variables de Entorno (Opcional)

Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-aqui
MYSQL_HOST=localhost
MYSQL_USER=pharmaflow_app
MYSQL_PASSWORD=AppPharma2024!
MYSQL_DATABASE=pharmaflow_relational
MONGODB_HOST=localhost
MONGODB_USER=pharmaflow_app
MONGODB_PASSWORD=AppMongo2024!
MONGODB_DATABASE=pharmaflow_nosql
```

### 7. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Usuarios de Prueba

### Gerente (Acceso Total)
- **Usuario:** `admin_gerente`
- **Contraseña:** `PharmaFlow123!`
- **Permisos:** Acceso completo a inventario, ventas, compras, usuarios y auditoría

### Farmacéutico (Operaciones de Venta)
- **Usuario:** `maria_farm`
- **Contraseña:** `PharmaFlow123!`
- **Permisos:** Registrar ventas, consultar inventario, actualizar lotes

### Investigador (Solo Lectura + Ensayos)
- **Usuario:** `ana_investigadora`
- **Contraseña:** `PharmaFlow123!`
- **Permisos:** Lectura de datos relacionales, acceso completo a ensayos clínicos

## Estructura del Proyecto

```
proyecto 2 bases de datos/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias Python
├── config/
│   ├── __init__.py
│   └── config.py              # Configuración de la aplicación
├── models/
│   ├── __init__.py
│   ├── database.py            # Gestor de conexiones
│   ├── mysql_models.py        # Modelos MySQL (ORM manual)
│   └── mongodb_models.py      # Modelos MongoDB (ODM manual)
├── utils/
│   ├── __init__.py
│   ├── security.py            # Funciones de seguridad
│   └── helpers.py             # Funciones auxiliares
├── templates/                  # Plantillas HTML
│   ├── login.html
│   ├── dashboard.html
│   ├── ventas.html
│   ├── ordenes_compra.html
│   ├── ensayos_clinicos.html
│   ├── reportes.html
│   └── usuarios.html
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── dashboard.js
│       ├── ventas.js
│       └── ensayos.js
└── database/                   # Scripts de base de datos
    ├── mysql_schema.sql       # Esquema MySQL
    ├── mysql_roles_privileges.sql  # Roles y permisos
    ├── mysql_data_seed.sql    # Datos iniciales MySQL
    ├── mongodb_setup.js       # Configuración MongoDB
    └── mongodb_seed.js        # Datos iniciales MongoDB
```

##  Seguridad Implementada

### Control de Acceso
- **Gerente:** Acceso total (CRUD en todas las tablas)
- **Farmacéutico:** Solo registro de ventas y actualización de lotes
- **Investigador:** Solo lectura en MySQL, CRUD en MongoDB

### Concurrencia
- Control de concurrencia optimista en ventas
- Campo `version` en tabla `lotes` para detectar conflictos
- Transacciones ACID en operaciones críticas

### Auditoría
- Triggers automáticos registran todas las operaciones
- Tabla `auditoria_transacciones` con datos antes/después
- Solo gerentes pueden consultar logs de auditoría

### Autenticación
- Contraseñas hasheadas con bcrypt
- Sesiones con timeout configurable
- Validación de credenciales en cada request

##  Funcionalidades Principales

### 1. Gestión de Inventario
- Visualizar stock actual
- Alertas de medicamentos próximos a caducar
- Control de lotes con trazabilidad completa

### 2. Sistema de Ventas
- Registro de ventas con múltiples productos
- Control de concurrencia para evitar sobreventa
- Actualización automática de inventario

### 3. Órdenes de Compra
- Crear órdenes de compra a proveedores
- Seguimiento de estado (Pendiente/Aprobada/Recibida)
- Cálculo automático de totales

### 4. Ensayos Clínicos (MongoDB)
- Registro flexible de ensayos en diferentes fases
- Seguimiento de participantes y resultados
- Documentación de efectos adversos

### 5. Reportes de Investigación
- Reportes mensuales de seguimiento
- Análisis de efectos adversos
- Reportes finales de estudios

### 6. Interacciones de Compuestos
- Base de conocimiento de interacciones medicamentosas
- Búsqueda por compuesto químico
- Niveles de severidad y recomendaciones

## Casos de Uso Implementados

### Caso 1: Control de Concurrencia en Ventas
Dos farmacéuticos intentan vender el mismo lote simultáneamente:

1. Farmacéutico A inicia venta del Lote-001 (10 unidades disponibles)
2. Farmacéutico B inicia venta del Lote-001 al mismo tiempo
3. A intenta vender 8 unidades → **Éxito** (quedan 2)
4. B intenta vender 5 unidades → **Falla** (conflicto de concurrencia)
5. B reintenta con 2 unidades → **Éxito**

### Caso 2: Roles y Permisos
```
Investigador intenta registrar una venta →  DENEGADO (403 Forbidden)
Farmacéutico intenta crear usuarios →  DENEGADO (403 Forbidden)
Gerente puede hacer ambas operaciones →  PERMITIDO
```

### Caso 3: Estructura Flexible en MongoDB
Ensayo Clínico puede tener campos variables:
```javascript
{
  trial_id: "CT-2024-001",
  resultados_preliminares: {
    // Campos personalizados por estudio
    tasa_curacion: 89.5,
    custom_metric_x: 123.45
  },
  notas_investigacion: [
    // Array dinámico de notas
  ]
}
```

##  Optimizaciones Implementadas

### MySQL
- **Índices:** En campos de búsqueda frecuente (nombre, fecha, estado)
- **Vistas:** Pre-calculadas para consultas complejas
- **Procedimientos Almacenados:** Lógica de negocio en BD
- **Pool de Conexiones:** Reutilización de conexiones

### MongoDB
- **Índices de Texto:** Búsqueda full-text en documentos
- **Índices Compuestos:** Optimización de consultas frecuentes
- **Agregación:** Pipeline para estadísticas

## Solución de Problemas

### Error: "Access denied for user"
```bash
# Verificar usuarios MySQL
mysql -u root -p
SELECT User, Host FROM mysql.user;

# Recrear usuario si es necesario
DROP USER 'pharmaflow_app'@'localhost';
source database/mysql_roles_privileges.sql
```

### Error: "Authentication failed" (MongoDB)
```bash
# Conectar sin autenticación
mongosh --noauth

# Verificar usuarios
use admin
db.getUsers()

# Recrear usuarios si es necesario
load('database/mongodb_setup.js')
```

### Error: "Module not found"
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

## Documentación Adicional

### API Endpoints

#### Autenticación
- `POST /login` - Iniciar sesión
- `GET /logout` - Cerrar sesión

#### Inventario
- `GET /api/inventario` - Listar inventario
- `GET /api/medicamentos` - Listar medicamentos
- `GET /api/lotes/caducar` - Medicamentos próximos a caducar

#### Ventas
- `GET /api/ventas` - Listar ventas
- `POST /api/ventas` - Registrar venta
- `GET /api/venta/<id>` - Detalle de venta

#### Ensayos Clínicos
- `GET /api/ensayos-clinicos` - Listar ensayos
- `POST /api/ensayos-clinicos` - Crear ensayo
- `GET /api/ensayo-clinico/<id>` - Detalle de ensayo

---

**PharmaFlow Solutions** - Sistema de Gestión Farmacéutica Integral
