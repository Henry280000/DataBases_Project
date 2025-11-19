# Guía de Instalación - PharmaFlow Solutions

## Requisitos Previos

Antes de ejecutar el script de instalación, asegúrate de tener instalado:

### 1. Python 3.9 o superior
```bash
python3 --version
```
Si no está instalado: https://www.python.org/downloads/

### 2. MySQL 8.0 o superior
```bash
mysql --version
```
Si no está instalado:
- **macOS**: `brew install mysql`
- **Linux**: `sudo apt-get install mysql-server`
- **Windows**: https://dev.mysql.com/downloads/installer/

**Importante**: Anota tu usuario y contraseña de MySQL root

### 3. MongoDB 6.0 o superior
```bash
mongosh --version
```
Si no está instalado:
- **macOS**: `brew tap mongodb/brew && brew install mongodb-community`
- **Linux**: https://www.mongodb.com/docs/manual/administration/install-on-linux/
- **Windows**: https://www.mongodb.com/try/download/community

### 4. Iniciar los servicios

**MySQL:**
```bash
# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```

**MongoDB:**
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

## Verificación Rápida de Requisitos

Ejecuta este comando para verificar que todo está listo:

```bash
./check_requirements.sh
```

Si todo está OK, continúa con la instalación.

## Instalación Paso a Paso

### 1. Clonar el repositorio
```bash
git clone https://github.com/Henry280000/DataBases_Project.git
cd DataBases_Project
```

### 2. Dar permisos de ejecución a los scripts
```bash
chmod +x install.sh
chmod +x start.sh
chmod +x check_requirements.sh
```

### 3. Ejecutar instalación
```bash
./install.sh
```

El script te pedirá:
- Usuario de MySQL (por defecto: root)
- Contraseña de MySQL

### 4. Si hay errores en MongoDB

Si el script se detiene en "Configurando MongoDB", verifica:

```bash
# Verificar que MongoDB está corriendo
mongosh --eval "db.version()"

# Si no está corriendo, iniciarlo
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

Luego ejecuta manualmente:
```bash
source venv/bin/activate
python database/mongodb_setup.py
python database/mongodb_seed.py
```

## Solución de Problemas Comunes

### Error: "No se pudo conectar a MySQL"
- Verifica que MySQL está corriendo: `mysql.server status` o `brew services list`
- Verifica usuario y contraseña: `mysql -u root -p`
- Si olvidaste la contraseña: https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html

### Error: "MySQL command not found"
- Agrega MySQL al PATH:
```bash
export PATH="/usr/local/mysql/bin:$PATH"
echo 'export PATH="/usr/local/mysql/bin:$PATH"' >> ~/.zshrc
```

### Error: "Connection refused" en MongoDB
- Verifica que MongoDB está corriendo: `brew services list`
- Inicia MongoDB: `brew services start mongodb-community`
- Espera 10 segundos y vuelve a intentar

### Error: "Permission denied" al crear venv
```bash
# macOS: Instala las herramientas de línea de comandos
xcode-select --install

# Verifica permisos
ls -la
```

### El script se congela en "Instalando dependencias"
- Cancela con Ctrl+C
- Instala manualmente:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Instalación Manual (Plan B)

Si el script automático falla, sigue estos pasos:

### 1. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar MySQL
```bash
mysql -u root -p < database/mysql_schema.sql
mysql -u root -p < database/mysql_roles_privileges.sql
mysql -u root -p < database/mysql_data_seed.sql
```

### 4. Configurar MongoDB
```bash
python database/mongodb_setup.py
python database/mongodb_seed.py
```

### 5. Crear directorios
```bash
mkdir -p logs uploads
```

### 6. Iniciar aplicación
```bash
python app.py
```

## Verificar Instalación

Abre tu navegador en: http://localhost:5001

Prueba con estas credenciales:
- **Gerente**: admin_gerente / Admin2024!
- **Farmacéutico**: maria_farm / Maria2024!
- **Investigador**: ana_investigadora / Ana2024!

## Siguiente Paso

Una vez instalado correctamente, usa:
```bash
./start.sh
```

Para iniciar la aplicación en el futuro.

## Soporte

Si sigues teniendo problemas:
1. Lee el archivo `COMANDOS_UTILES.md`
2. Revisa los logs en la carpeta `logs/`
3. Verifica que todos los servicios estén corriendo
