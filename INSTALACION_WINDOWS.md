# Guia de Instalacion para Windows

## Requisitos Previos

Antes de instalar, asegurate de tener:

1. **Python 3.9 o superior**
   - Descarga: https://www.python.org/downloads/
   - Durante la instalacion, MARCA la casilla "Add Python to PATH"

2. **MySQL Community Server 8.0**
   - Descarga: https://dev.mysql.com/downloads/installer/
   - Selecciona "MySQL Server" y "MySQL Workbench" (opcional)
   - Anota la contraseña de root que configures

3. **MongoDB Community Edition**
   - Descarga: https://www.mongodb.com/try/download/community
   - Instala como servicio de Windows (opcion por defecto)

4. **Git para Windows** (opcional)
   - Descarga: https://git-scm.com/download/win
   - Solo necesario si vas a clonar desde GitHub

## Verificacion Rapida

Abre **PowerShell o CMD** y ejecuta:

```batch
check_requirements.bat
```

Esto verificara todos los requisitos y te dira que falta.

## Instalacion Automatica

### Paso 1: Descargar el Proyecto

**Opcion A: Con Git**
```batch
git clone https://github.com/Henry280000/DataBases_Project.git
cd DataBases_Project
```

**Opcion B: Sin Git**
1. Ve a https://github.com/Henry280000/DataBases_Project
2. Click en "Code" → "Download ZIP"
3. Extrae el ZIP en una carpeta
4. Abre CMD en esa carpeta

### Paso 2: Ejecutar Instalador

1. **Haz clic derecho** en `install.bat`
2. Selecciona **"Ejecutar como administrador"**
3. Ingresa la contraseña de root de MySQL cuando se solicite
4. Espera a que termine (2-5 minutos)

### Paso 3: Iniciar la Aplicacion

Doble click en `start.bat` o ejecuta:
```batch
start.bat
```

Abre tu navegador en: **http://localhost:5001**

## Credenciales por Defecto

- **Administrador**: admin / admin123
- **Medico**: medico / medico123
- **Farmaceutico**: farmaceutico / farmaceutico123

## Solucion de Problemas

### Error: "Python no esta instalado"
- Reinstala Python desde https://www.python.org/downloads/
- IMPORTANTE: Marca "Add Python to PATH"
- Reinicia CMD/PowerShell despues de instalar

### Error: "MySQL no esta instalado"
- Descarga MySQL Installer: https://dev.mysql.com/downloads/installer/
- Selecciona "Developer Default" o al menos "MySQL Server"
- Durante la configuracion, crea una contraseña de root

### Error: "MySQL no esta corriendo"
Abre "Servicios" de Windows (services.msc) y busca:
- MySQL80
- Haz clic derecho → Iniciar

O desde CMD como administrador:
```batch
net start MySQL80
```

### Error: "MongoDB no esta corriendo"
Abre "Servicios" de Windows (services.msc) y busca:
- MongoDB
- Haz clic derecho → Iniciar

O desde CMD como administrador:
```batch
net start MongoDB
```

### Error: "Access denied for user"
La contraseña de MySQL root es incorrecta.

Solucion:
1. Abre MySQL Workbench
2. Conectate con la contraseña correcta
3. Vuelve a ejecutar install.bat con la contraseña correcta

### Error: "pip no se reconoce"
Python no esta en el PATH.

Solucion:
1. Busca donde esta instalado Python (ej: C:\Python39)
2. Agrega a PATH:
   - Inicio → "variables de entorno"
   - Editar PATH
   - Agregar: C:\Python39 y C:\Python39\Scripts
3. Reinicia CMD

### Error: "No se pudo crear el entorno virtual"
Problemas con permisos.

Solucion:
1. Cierra todas las ventanas de CMD/PowerShell
2. Haz clic derecho en install.bat
3. "Ejecutar como administrador"

### La aplicacion no inicia
Verifica que los servicios esten corriendo:
```batch
sc query MySQL80
sc query MongoDB
```

## Comandos Utiles

### Ver estado de servicios
```batch
sc query MySQL80
sc query MongoDB
```

### Iniciar servicios manualmente
```batch
net start MySQL80
net start MongoDB
```

### Detener servicios
```batch
net stop MySQL80
net stop MongoDB
```

### Acceder a MySQL desde CMD
```batch
mysql -u root -p
# Ingresa tu contraseña de root
```

### Verificar base de datos
```batch
mysql -u pharmaflow_app -p pharmaflow_relational
# Contraseña: AppPharma2024!

# Dentro de MySQL:
SHOW TABLES;
SELECT COUNT(*) FROM usuarios;
```

## Desinstalacion

1. Detener la aplicacion (Ctrl+C en la ventana donde corre)
2. Eliminar la carpeta del proyecto
3. (Opcional) Eliminar base de datos:
```sql
DROP DATABASE pharmaflow_relational;
```

## Reinstalacion Limpia

Si quieres empezar de cero:

1. Elimina la carpeta `venv`
2. Elimina el archivo `.env`
3. En MySQL, ejecuta:
```sql
DROP DATABASE IF EXISTS pharmaflow_relational;
DROP USER IF EXISTS 'pharmaflow_app'@'localhost';
```
4. En MongoDB:
```javascript
use pharmaflow_nosql
db.dropDatabase()
```
5. Ejecuta `install.bat` como administrador

## Soporte

Si encuentras problemas:
1. Verifica requisitos: `check_requirements.bat`
2. Revisa los logs en la ventana donde corre la aplicacion
3. Asegurate de que MySQL y MongoDB esten corriendo

## Notas Adicionales

- La primera instalacion puede tardar 5-10 minutos
- Los datos de prueba se cargan automaticamente
- El puerto 5001 debe estar libre
- Necesitas conexion a internet para descargar paquetes Python
