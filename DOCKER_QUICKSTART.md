# PharmaFlow Solutions - Instalación con Docker

## Requisitos

Solo necesitas **Docker Desktop** instalado:
- **Windows/Mac**: https://www.docker.com/products/docker-desktop
- **Linux**: https://docs.docker.com/engine/install/

## Instalación en 3 Pasos

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Henry280000/DataBases_Project.git
cd DataBases_Project
```

### 2. Iniciar los Contenedores
```bash
docker-compose up -d
```

### 3. Acceder a la Aplicación
Abre tu navegador en: **http://localhost:5001**

## Credenciales

- **Administrador**: admin / admin123
- **Médico**: medico / medico123
- **Farmacéutico**: farmaceutico / farmaceutico123

## Comandos Útiles

### Ver estado de contenedores
```bash
docker-compose ps
```

### Ver logs
```bash
docker-compose logs -f
```

### Detener la aplicación
```bash
docker-compose down
```

### Reiniciar todo (con datos limpios)
```bash
docker-compose down -v
docker-compose up -d
```

### Actualizar código
```bash
git pull
docker-compose up -d --build
```

## Verificación

Verifica que todo funciona:

```bash
# Ver contenedores corriendo
docker-compose ps

# Verificar MySQL
docker-compose exec mysql mysql -u pharmaflow_user -ppharmaflow123 -e "SHOW DATABASES;"

# Verificar MongoDB
docker-compose exec mongodb mongosh -u admin -p admin123 --eval "show dbs"

# Ver logs de la app
docker-compose logs app
```

## Solución de Problemas

### Puerto ocupado (ERROR MÁS COMÚN)

**Si tienes MySQL o MongoDB instalados localmente**, los puertos estarán ocupados.

**SOLUCIÓN**: El proyecto ya usa puertos alternativos:
- MySQL Docker: Puerto **3307** (en lugar de 3306)
- MongoDB Docker: Puerto **27018** (en lugar de 27017)
- Flask: Puerto **5001** (libre normalmente)

Esto evita conflictos con instalaciones locales. La aplicación se conecta automáticamente a los contenedores.

Si aún tienes conflictos, cambia en `docker-compose.yml`:
```yaml
ports:
  - "3308:3306"  # MySQL en puerto 3308
  - "27019:27017"  # MongoDB en puerto 27019
  - "5002:5001"  # Flask en puerto 5002
```

### Contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs mysql
docker-compose logs mongodb
docker-compose logs app
```

### Resetear todo
```bash
docker-compose down -v
docker system prune -a
docker-compose up -d
```

### Acceder a las bases de datos

**MySQL** (desde el contenedor):
```bash
docker-compose exec mysql mysql -u pharmaflow_user -ppharmaflow123 pharmaflow_relational
```

**MySQL** (desde tu máquina):
```bash
mysql -h 127.0.0.1 -P 3307 -u pharmaflow_user -ppharmaflow123 pharmaflow_relational
```

**MongoDB** (desde el contenedor):
```bash
docker-compose exec mongodb mongosh -u admin -p admin123 pharmaflow_nosql
```

**MongoDB** (desde tu máquina):
```bash
mongosh mongodb://admin:admin123@localhost:27018/pharmaflow_nosql
```

## Ventajas de Docker

- No necesitas instalar MySQL, MongoDB ni Python
- Funciona igual en Windows, Mac y Linux
- Aislado de tu sistema
- Fácil de eliminar completamente
- Bases de datos se inicializan automáticamente con datos

## Arquitectura

```
┌─────────────────────────┐
│  pharmaflow_app         │
│  Flask (Puerto 5001)    │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │               │
┌───▼────┐    ┌────▼─────┐
│ MySQL  │    │ MongoDB  │
│ :3306  │    │ :27017   │
└────────┘    └──────────┘
```

## Transferir a Otro Dispositivo

Simplemente clona el repo y ejecuta `docker-compose up -d` en la nueva máquina.

## Desinstalar

```bash
docker-compose down -v
docker rmi databases_project_app mysql:8.0 mongo:6.0
```

## Soporte

Si tienes problemas:
1. Asegúrate que Docker Desktop esté corriendo
2. Ejecuta `docker-compose logs -f` para ver errores
3. Prueba `docker-compose down -v && docker-compose up -d`
