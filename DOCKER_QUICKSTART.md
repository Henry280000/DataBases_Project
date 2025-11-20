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

### Puerto ocupado
Si el puerto 5001, 3306 o 27017 está ocupado, edita `docker-compose.yml`:
```yaml
ports:
  - "5002:5001"  # Cambiar puerto externo
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

**MySQL**:
```bash
docker-compose exec mysql mysql -u pharmaflow_user -ppharmaflow123 pharmaflow_relational
```

**MongoDB**:
```bash
docker-compose exec mongodb mongosh -u admin -p admin123 pharmaflow_nosql
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
